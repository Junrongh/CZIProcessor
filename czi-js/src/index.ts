import CZIReader from "./CZIReader";

const canvas = document.getElementById('mycanvas');

const reader = new CZIReader();

reader.test();
reader.load('./dist/public/EPSC-em1_CK18_10x.czi').then(res => {
    console.log(res);
})
window['reader'] = reader;
