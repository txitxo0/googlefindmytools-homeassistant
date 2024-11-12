from FMDNCrypto.eid_generator import generate_eid, ROTATION_PERIOD
from FMDNCrypto.key_derivation import FMDNOwnerOperations
from FMDNCrypto.util import calculate_hmac_sha256
from private import sample_identity_key, sample_account_key

ownerOperations = FMDNOwnerOperations()
ownerOperations.generate_keys(sample_identity_key)

def getOwnerLoopUpLink(eik, offset):

    recoveryKey = ownerOperations.recovery_key
    eid = generate_eid(eik, offset).to_bytes(20, 'big')

    truncated_ephemeral_id = eid[:10]
    hmac = calculate_hmac_sha256(recoveryKey, truncated_ephemeral_id)

    hmac_truncated = hmac[:16]

    return (eid.hex(), 'https://spot-pa.googleapis.com/lookup?e=' + truncated_ephemeral_id.hex() + hmac_truncated)

if __name__ == '__main__':
    # Generate a few URLs
    for i in range(1000):
        offset = i*ROTATION_PERIOD
        print(getOwnerLoopUpLink(sample_identity_key, offset))