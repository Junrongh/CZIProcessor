import CZIReader from "./CZIReader";

const canvas = document.getElementById('mycanvas');

const reader = new CZIReader();

reader.test();
window['reader'] = reader;
