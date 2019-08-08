function buscar_item(text) {
    var resultado = document.querySelectorAll("body");

    for (i = 0; i < resultado.length; i++) {
        console.log(resultado[i]);
    }
    if (text.length > 0) {
        console.log("buscar_item", text);
        get_json(URL_BUSCA + "?texto=" + text, tratar_resultado_busca);
    }
}

function tratar_resultado_busca(json) {
    console.log("tratar_resultado_busca", json);
}
document.addEventListener('keydown', function (event) {
    switch (event.keyCode) {
        case 13: //ENTER
        case 27: //ESC
        case 112: //F1
        case 113:
        case 114:
        case 115:
            //case 116:
        case 117:
        case 118:
        case 119:
        case 120:
        case 121:
            //case 122:
        case 123: //F12
            //case 37: // ESQUERDA
        case 38: // CIMA
            //case 39: // DIREITA
        case 40: // BAIXO
            event.preventDefault();

        default:
            console.log(event.keyCode);
    }
});