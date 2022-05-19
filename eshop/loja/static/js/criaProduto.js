/** este javascript serve para adicionar input de nova questão quando se clica no botão de adicionar e para adicionar opcoes por baixo da respetiva questao */
    var q=0;

    $(document).on('change', '.checkbox', function() {   
        if(this.checked ) {
            var test = $('<input/>', { type: 'submit', class: 'remover', value: 'Adiciona Questão', click: function () { Cria_Questao(); } });
            $('#question').append(test).end();
            Cria_Questao();
        }else{
                $('.remover').remove();
                q=0;
        }
        });

    function Cria_Questao(){
        q++;
        var nrQuestao=q;
        if(q>4){
            alert("nao pode criar mais");
        }else{
            var add_op = $('<input/>', { type: 'submit', value: 'Adiciona Opção', class: 'remover', text: 'Adiciona Opção', click: function () { adicionarOp(nrQuestao) ; }});
            label="<label  class=remover for=questao"+(q)+"'><b>Questão:</b></label>"
            input = jQuery('<input class="remover form-control" type="text" id="questao_'+(q)+'" name="questao" required>');
            btnEliminaQ = '<button class=remover id="eliminaQ" onclick="Elimina_Questao('+nrQuestao+');"> Eliminar Questão </button>'
            jQuery("#questao_"+q).append("<br class=remover>"+label).append(input).append(add_op).append(btnEliminaQ).append("<br class=remover>");
            adicionarOp(nrQuestao);
        }
    
    }

    function Elimina_Questao(nrQue){
        const myNode = document.getElementById("#questao_" + nrQue);
        myNode.innerHTML = '';
        q--;
    } 
    
    function adicionarOp(nrOpcao){
        inputi = jQuery('<input class="remover form-control" type="text" id="opcao_'+(nrOpcao)+'" name="questao_'+(nrOpcao)+'" required>');
        jQuery("#questao_"+nrOpcao).append("<label  class=remover for=opcao_"+(nrOpcao)+"'><b>Opção:</b></label> ").append(inputi).append("<br class=remover>");
    }
 
