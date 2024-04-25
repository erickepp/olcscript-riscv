function SaveOutputButton({ output }) {

    const handleSaveOutput = async () => {
      try {
        const handle = await window.showSaveFilePicker({
          suggestedName: 'riscv.s',
          types: [{
            description: 'Text file',
            accept: { 'text/plain': ['.s'] },
          }]
        });
        const writable = await handle.createWritable();
        await writable.write(output);
        await writable.close();
      } catch (err) {
        console.error(err.name, err.message);
      }
    };
  
    return (
      <button
        type="button"
        class="btn btn-secondary"
        style={{ width: "100%", overflow: "hidden" }}
        onClick={handleSaveOutput}
      >
        Guardar
      </button>
    );
    
  }
  
  export default SaveOutputButton;
  