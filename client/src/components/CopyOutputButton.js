function CopyOutputButton({ output }) {

    const handleCopyOutput = async () => {
        const copyButton = document.getElementById('btn-copy');

        try {
            await navigator.clipboard.writeText(output);
            copyButton.innerText = 'Copiado';
        } catch (err) {
            copyButton.innerText = 'Error';
            console.error('Error al copiar: ', err);
        }

        setTimeout(() => {
            copyButton.innerText = 'Copiar';
        }, 300);
    };
  
    return (
      <button
        id="btn-copy"
        type="button"
        class="btn btn-secondary"
        style={{ width: "100%", overflow: "hidden" }}
        onClick={handleCopyOutput}
      >
        Copiar
      </button>
    );
    
  }
  
  export default CopyOutputButton;
  