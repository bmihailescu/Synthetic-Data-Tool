const submit = document.querySelector("#submit")

submit.addEventListener("click",progressBar)

function progressBar() {
    const num_of_columns =  document.querySelectorAll("[id^='row']").length
    const num_of_entries = parseInt(document.querySelector("#num_of_entries").value)
    const num_of_cells = num_of_columns * num_of_entries

    const progress_bar = document.querySelector("#progress_bar")
    width=0


    if (isNaN(num_of_cells) == false) {
        var id = setInterval(frame, num_of_cells/25);
    }

    function frame() {
      if (width == 100) {
        clearInterval(id);
        setTimeout(() => {  progress_bar.style.width = "0" + '%'; }, 3000);
        
    } 
      else {width++;
            progress_bar.style.width = width + '%';
      }
    }
    
}