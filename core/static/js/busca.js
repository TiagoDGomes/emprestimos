var busca_em_execucao = false;
var tabela;
var index_selecionado = -1;
var contador_resultado = 0;
var item_pesquisa;
var json_resultado_atual;
var pessoa_selecionada = null;
var itens_selecionados = [];

document.addEventListener("DOMContentLoaded", function (event) {
    console.log("DOM completamente carregado e analisado");
    tabela = document.getElementById('tabela-resultado-corpo');
    item_pesquisa = document.getElementById('item_pesquisa');
    item_pesquisa.addEventListener('keyup', function (event) {
        switch (event.keyCode) {
            case 13: // ENTER
            case 37: // ESQUERDA
            case 38: // CIMA
            case 39: // DIREITA       
            case 40: // BAIXO
            case 27: //ESC
            case 112: //F1
            case 113: // f2        
            case 115: // F4
            case 117: // F6
            case 118: // F7
            case 119: // F8
            case 120: // F9
            case 121: // F10
            case 123: // F12
                event.preventDefault();
                break;
            default:
                buscar_item(item_pesquisa);
                console.log('item_pesquisa', event.keyCode);
        }
    });
    document.addEventListener('keyup', function (event) {
        var tabela_lista_emprestimos = document.getElementById('lista_emprestimos_corpo');
        switch (event.keyCode) {
            //case 116: // F5
            //case 122: // F11
            //case 37: // ESQUERDA
            //case 39: // DIREITA
            case 114: // F3
                document.getElementById('item_pesquisa').focus();
                event.preventDefault();
                break;
            case 38: // CIMA
                if (index_selecionado > 0) {
                    atual = index_selecionado - 1;
                    selecionar(atual);
                }
                event.preventDefault();
                break;
            case 40: // BAIXO
                if (index_selecionado < contador_resultado - 1) {
                    atual = index_selecionado + 1;
                    selecionar(atual);
                }
                event.preventDefault();
                break;
            case 13: //ENTER
                event.preventDefault();
                atual = document.getElementById('resultado_' + index_selecionado);
                var pessoa = json_resultado_atual['pessoas'][atual.dataset.index];
                if (atual.dataset.tipo == 'pessoa') {
                    var definir_pessoa = true;
                    if (pessoa_selecionada != null && pessoa_selecionada != pessoa) {
                        if (!confirm('Já existe uma pessoa selecionada. Todos os itens já marcados serão excluídos. Deseja continuar?')) {
                            definir_pessoa = false;
                        } else {
                            while (tabela_lista_emprestimos.hasChildNodes()) {
                                console.log(tabela_lista_emprestimos.hasChildNodes());
                                tabela_lista_emprestimos.removeChild(tabela_lista_emprestimos.firstChild)
                            }
                            itens_selecionados = [];
                        }
                    }
                    if (definir_pessoa) {
                        var card_header = document.querySelectorAll('.responsavel.card .card-header')[0];
                        var card_body = document.querySelectorAll('.responsavel.card .card-body')[0];
                        var card_footer = document.querySelectorAll('.responsavel.card .card-footer')[0];
                        card_header.classList.add('bg-primary');
                        card_header.classList.add('text-white');
                        card_body.classList.add('bg-primary');
                        card_body.classList.add('text-white');
                        card_footer.classList.add('bg-primary');
                        card_footer.classList.add('text-white');
                        card_body.innerHTML = pessoa.nome;
                        pessoa_selecionada = pessoa;
                    }

                } else {
                    var item = json_resultado_atual['itens'][atual.dataset.index];
                    var tr = document.createElement('tr');
                    var td_data = document.createElement('td');
                    var td_nome = document.createElement('td');
                    var td_status = document.createElement('td');
                    td_nome.innerHTML = item['nome'];
                    tr.appendChild(td_data);
                    tr.appendChild(td_nome);
                    tr.appendChild(td_status);
                    tabela_lista_emprestimos.insertBefore(tr, tabela_lista_emprestimos.childNodes[0]);
                    itens_selecionados.push(item);
                }
                break;
            case 27: //ESC
            case 112: //F1
            case 113: // f2        
            case 115: // F4
            case 117: // F6
            case 118: // F7
            case 119: // F8
            case 120: // F9
            case 121: // F10
            case 123: // F12
                event.preventDefault();
                break;
        }
    });
});

function selecionar(index) {
    try {
        anterior = document.getElementById('resultado_' + index_selecionado);
        anterior.classList.remove('selecionado');
    } catch (e) {}
    atual = document.getElementById('resultado_' + index);
    atual.classList.add('selecionado');
    index_selecionado = index * 1;
    item_pesquisa.setSelectionRange(0, item_pesquisa.value.length)
}

function buscar_item(obj_input) {
    index_selecionado = -1;
    if (obj_input.value.length > 0 && busca_em_execucao == false) {
        console.log("buscar_item", obj_input.value);
        busca_em_execucao = true;
        setTimeout(function () {
            get_json(URL_BUSCA + "?texto=" + obj_input.value, tratar_resultado_busca);
        }, 700);
    }
}


function tratar_resultado_busca(json) {
    busca_em_execucao = false;
    json_resultado_atual = json;
    tabela.innerHTML = '';
    contador_resultado = 0;
    for (i = 0; i < json.pessoas.length; i++) {
        var tr = document.createElement('tr'); // Linha
        var pessoa = json.pessoas[i];
        tr.id = 'resultado_' + contador_resultado++;
        tr.dataset.index = i;
        tr.dataset.pid = contador_resultado - 1;
        tr.dataset.info = pessoa;
        tr.dataset.tipo = 'pessoa';
        tr.onclick = function () {
            selecionar(this.dataset.pid);
        }
        var td_codigo = document.createElement('td'); // celula código
        var td_nome = document.createElement('td'); // celula nome
        var td_detalhes = document.createElement('td'); // celula detalhes
        td_codigo.innerHTML = pessoa.matricula;
        td_nome.innerHTML = pessoa.nome;

        if (pessoa.bloqueio != null) {
            td_nome.style.textDecoration = 'line-through'
        }
        tr.appendChild(td_codigo);
        tr.appendChild(td_nome);
        tr.appendChild(td_detalhes);
        tabela.appendChild(tr);
    }
    for (i = 0; i < json.itens.length; i++) {
        var tr = document.createElement('tr'); // Linha
        var item = json.itens[i];
        tr.id = 'resultado_' + contador_resultado++;
        tr.dataset.pid = contador_resultado - 1;
        tr.dataset.index = i;
        tr.dataset.tipo = 'item';
        tr.onclick = function () {
            selecionar(this.dataset.pid);
        }
        tr.dataset.info = item;
        var td_codigo = document.createElement('td'); // celula código
        var td_nome = document.createElement('td'); // celula nome
        var td_detalhes = document.createElement('td'); // celula detalhes
        td_codigo.innerHTML = item.codigo;
        td_nome.innerHTML = item.nome;
        tr.appendChild(td_codigo);
        tr.appendChild(td_nome);
        tr.appendChild(td_detalhes);
        tabela.appendChild(tr);
    }
    if (json.pessoas.length + json.itens.length == 1) {
        tr.classList.add('selecionado');
        index_selecionado = 0;
    }

}