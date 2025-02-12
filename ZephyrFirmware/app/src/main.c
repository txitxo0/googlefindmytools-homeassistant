#include <stddef.h>
#include <zephyr/sys/printk.h>
#include <zephyr/sys/util.h>
#include <zephyr/types.h>
#include <zephyr/logging/log.h>

#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/bluetooth/hci.h>

LOG_MODULE_REGISTER(main, CONFIG_APP_LOG_LEVEL);

// This is the advertisement key / EID. Change it to your own EID.
const char *eid_string = "INSERT_YOUR_ADVERTISEMENT_KEY_HERE";

void hex_string_to_bytes(const char *hex, uint8_t *bytes, size_t len) {
  for (size_t i = 0; i < len; i++) {
    sscanf(hex + 2 * i, "%2hhx", &bytes[i]);
  }
}

struct bt_le_adv_param adv_param = {
    .options = BT_LE_ADV_OPT_USE_IDENTITY,
    /* Advertising interval in 0.625ms steps: 3200*0.625ms=2s */
    .interval_min = 3200,
    .interval_max = 3200,
};

typedef struct __attribute__((packed)) {
  uint8_t flags_data;
} fmdn_flags_data_t;

/* Adv Frame, see https://developers.google.com/nearby/fast-pair/specifications/extensions/fmdn#advertised-frames */
typedef struct __attribute__((packed)) {
  uint16_t service_uuid;
  uint8_t frame_type;
  uint8_t eid[20];
  uint8_t hashed_flags;
} fmdn_service_data_t;

fmdn_flags_data_t fmdn_flags_data = {.flags_data = 0x06};
fmdn_service_data_t fmdn_service_data = {.service_uuid = 0xFEAA, .frame_type = 0x41, .hashed_flags = 0x0};

static const struct bt_data adv_data[] = {
    BT_DATA(BT_DATA_FLAGS, (unsigned char *)&fmdn_flags_data, sizeof(fmdn_flags_data)),
    BT_DATA(BT_DATA_SVC_DATA16, (unsigned char *)&fmdn_service_data, sizeof(fmdn_service_data)),

};

int main(void) {
  int err;

  hex_string_to_bytes(eid_string, fmdn_service_data.eid, 20);

  err = bt_enable(NULL);
  if (err) {
    LOG_ERR("Bluetooth init failed (err %d)\n", err);
    return 0;
  }

  printk("Bluetooth initialized\n");

  err = bt_le_adv_start(&adv_param, adv_data, ARRAY_SIZE(adv_data), NULL, 0);
  if (err) {
    LOG_ERR("Advertising failed to start (err %d)", err);
    return 0;
  }
}
