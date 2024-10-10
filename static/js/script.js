document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("formExpressao");
    const input = document.querySelector('input[name="expressao"]');
    const errorDiv = document.createElement("div");
    errorDiv.classList.add("erro");
    input.parentNode.appendChild(errorDiv);

    // Função para enviar o formulário via AJAX
    form.addEventListener("submit", function(event) {
        event.preventDefault(); // Evita o envio padrão do formulário
        const expressao = input.value.trim();

        if (!validarExpressao(expressao)) {
            errorDiv.textContent = "Expressão inválida. Verifique a sintaxe.";
            return;
        } else {
            errorDiv.textContent = ""; // Limpa mensagens de erro anteriores
        }

        const formData = new FormData(form);

        fetch("/", {
            method: "POST",
            body: formData,
        })
        .then(response => response.text())
        .then(html => {
            document.body.innerHTML = html; // Atualiza o conteúdo da página com o resultado
        })
        .catch(error => console.error("Erro:", error));
    });

    // Função para validar a expressão lógica no frontend
    function validarExpressao(expressao) {
        // Verificar parênteses balanceados
        let pilha = [];
        for (let char of expressao) {
            if (char === '(') {
                pilha.push(char);
            } else if (char === ')') {
                if (pilha.length === 0) return false;
                pilha.pop();
            }
        }
        if (pilha.length !== 0) return false;

        // Validação básica de operadores lógicos
        const operadores = /[^pqrsandorxor∧∨¬→↔⊕() ]/g;
        return !operadores.test(expressao);
    }
});
