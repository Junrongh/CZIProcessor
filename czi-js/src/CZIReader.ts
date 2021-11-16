export default class CZIReader {
    buffer: ArrayBuffer = null;
    constructor() {}

    public async load(src: string) {
        const response = await fetch(src);
        const ab = await response.arrayBuffer();
        const dec = new TextDecoder()
        const header = dec.decode(ab.slice(0, 10));
        if (header === 'ZISRAWFILE') {
            this.buffer = ab;
            return ab;
        } else {
            console.error('Error: not a czi file');
            return;
        }
    }

    public test() {
        console.log('test');
    }
}