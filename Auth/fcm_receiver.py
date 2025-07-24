import asyncio
import base64
import binascii
from auth.firebase_messaging import FcmRegisterConfig, FcmPushClient
from auth.token_cache import set_cached_value, get_cached_value

class FcmReceiver:
    _instance = None
    _listening = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(FcmReceiver, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        
        # Define Firebase project configuration
        project_id = "google.com:api-project-289722593072"
        app_id = "1:289722593072:android:3cfcf5bc359f0308"
        api_key = "AIzaSyD_gko3P392v6how2H7UpdeXQ0v2HLettc"
        message_sender_id = "289722593072"
        fcm_config = FcmRegisterConfig(
            project_id=project_id,
            app_id=app_id,
            api_key=api_key,
            messaging_sender_id=message_sender_id,
            bundle_id="com.google.android.apps.adm",
        )
        self.credentials = get_cached_value('fcm_credentials')
        self.location_update_callbacks = []
        self.pc = FcmPushClient(self._on_notification, fcm_config, self.credentials, self._on_credentials_updated)
        self.listen_task = None
        self.timeout_task = None
    
    def register_for_location_updates(self, callback, timeout_seconds=120):
        if not self._listening:
            asyncio.get_event_loop().run_until_complete(
                self._register_for_fcm_and_listen(timeout_seconds)
            )
        self.location_update_callbacks.append(callback)
        return self.credentials['fcm']['registration']['token']
    
    def stop_listening(self):
        if self.timeout_task and not self.timeout_task.done():
            self.timeout_task.cancel()
        if self.listen_task and not self.listen_task.done():
            self.listen_task.cancel()
        asyncio.get_event_loop().run_until_complete(self.pc.stop())
        self._listening = False
    
    def get_android_id(self):
        if self.credentials is None:
            return asyncio.get_event_loop().run_until_complete(
                self._register_for_fcm_and_listen()
            )
        return self.credentials['gcm']['android_id']
    
    # Define a callback function for handling notifications
    def _on_notification(self, obj, notification, data_message):
        # Reset the timeout timer when we receive a notification
        if self.timeout_task and not self.timeout_task.done():
            self.timeout_task.cancel()
        
        # Check if the payload is present
        if 'data' in obj and 'com.google.android.apps.adm.FCM_PAYLOAD' in obj['data']:
            # Decode the base64 string
            base64_string = obj['data']['com.google.android.apps.adm.FCM_PAYLOAD']
            decoded_bytes = base64.b64decode(base64_string)
            # Convert to hex string
            hex_string = binascii.hexlify(decoded_bytes).decode('utf-8')
            for callback in self.location_update_callbacks:
                callback(hex_string)
        else:
            print("[FCMReceiver] Payload not found in the notification.")
    
    def _on_credentials_updated(self, creds):
        self.credentials = creds
        # Also store to disk
        set_cached_value('fcm_credentials', self.credentials)
        print("[FCMReceiver] Credentials updated.")
    
    async def _timeout_handler(self, timeout_seconds):
        try:
            await asyncio.sleep(timeout_seconds)
            print(f"[FCMReceiver] Timed out after {timeout_seconds} seconds")
            if self._listening:
                await self.pc.stop()
                self._listening = False
        except asyncio.CancelledError:
            # This is normal when a notification is received and the timeout is canceled
            pass
    
    async def _register_for_fcm(self):
        fcm_token = None
        # Register or check in with FCM and get the FCM token
        while fcm_token is None:
            try:
                fcm_token = await self.pc.checkin_or_register()
            except Exception as e:
                await self.pc.stop()
                print(f"[FCMReceiver] Failed to register with FCM: {str(e)}. Retrying...")
                await asyncio.sleep(5)
    
    async def _register_for_fcm_and_listen(self, timeout_seconds=120):
        await self._register_for_fcm()
        
        self.listen_task = asyncio.create_task(self.pc.start())
        self._listening = True
        print("[FCMReceiver] Listening for notifications. This can take a few seconds...")
        
        # Set up the timeout
        if timeout_seconds > 0:
            self.timeout_task = asyncio.create_task(self._timeout_handler(timeout_seconds))

if __name__ == "__main__":
    receiver = FcmReceiver()
    try:
        # Example usage with a 30-second timeout
        def on_location_update(hex_data):
            print(f"Received location update: {hex_data[:20]}...")
        
        receiver.register_for_location_updates(on_location_update, timeout_seconds=30)
        # Keep the main thread running
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("Stopping...")
        receiver.stop_listening()