type Device = {
    id: Number,
    name: String,
    type: String,
    connection: String,
    fields: {
        key: String,
        value: String
    }
}

const deviceTypes: String[] = [
    "ble",
    "ade",
    "wifi"
]

export type { Device }
export { deviceTypes }