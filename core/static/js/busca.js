var busca_em_execucao = false;
function buscar_item(obj_input) {
    var resultado = document.querySelectorAll("body");

    if (obj_input.value.length > 0 && busca_em_execucao == false) {
        console.log("buscar_item", obj_input.value);
        busca_em_execucao = true;
        setTimeout(function(){            
            get_json(URL_BUSCA + "?texto=" + obj_input.value, tratar_resultado_busca);
        },700);        
    }
}

function tratar_resultado_busca(json) {
    busca_em_execucao = false;
    console.log("tratar_resultado_busca", json);
    var tabela = document.getElementById('tabela-resultado-corpo');
    tabela.innerHTML = '';
    var tr = document.createElement('tr'); // Linha
    tabela.appendChild(tr);
    for (i = 0; i < json.pessoas.length; i++){
        var pessoa = json.pessoas[i];
        var td_codigo = document.createElement('td'); // celula código
        var td_nome =  document.createElement('td'); // celula nome
        var td_detalhes =  document.createElement('td'); // celula detalhes
        td_codigo.innerHTML = pessoa.matricula;
        td_nome.innerHTML = pessoa.nome;
        
        if (pessoa.bloqueio != null){
            td_nome.style.textDecoration = 'line-through'
        }
        tr.appendChild(td_codigo);
        tr.appendChild(td_nome);
        tr.appendChild(td_detalhes); 
    }   
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