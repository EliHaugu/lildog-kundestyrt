type Device = {
    id: number,
    name: string,
    type: string,
    connection: string,
    fields: {
        key: string,
        value: string
    }
}

export type { Device }