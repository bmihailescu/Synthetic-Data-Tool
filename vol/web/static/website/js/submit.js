const submit = document.querySelector("#submit")

//////////// Custom Formats ////////////

submit.addEventListener("click",dateFormat)
submit.addEventListener("click",numberFormat)

// Concatenate all date format fields into one hidden field for ease of use in POST request
function dateFormat(e) {
    document.querySelectorAll("#dateFormat").forEach(element => {
        const dateDiv =  element.previousElementSibling.previousElementSibling
        const formatDate = dateDiv.nextElementSibling.lastElementChild.value
        const startDate = dateDiv.firstElementChild.firstElementChild.value
        const endDate = dateDiv.lastElementChild.firstElementChild.value

        element.value = formatDate + "," + startDate  + "," + endDate     
    });    
}

// Concatenate number format fields into one hidden field
function numberFormat(e) {
    document.querySelectorAll("#numberFormat").forEach(element => {
        const minNumber =  element.previousElementSibling.previousElementSibling.value
        const maxNumber =  element.previousElementSibling.value

        element.value = minNumber + "," + maxNumber
    });    
}

//////////// Form Validation ////////////
// const myForm = document.querySelector("#myForm")
// myForm.addEventListener("submit",function validateForm(e) {
//     const dataTypeDisplayValue = this.querySelectorAll("#dataTypeDisplayValue");
//     dataTypeDisplayValue.forEach(element => {
//         console.log(element.nextElementSibling.value)
//         if (element.text == "Email") {
//             // element.className = "nav-link dropdown-toggle invalid"
//             // console.log(element.nextElementSibling)
//             // e.preventDefault();
//             // e.stopPropagation();  
//         }
//     });
// });



// (function() {
//     'use strict';
//     window.addEventListener('load', function() {
//       // Fetch all the forms we want to apply custom Bootstrap validation styles to
//       var forms = document.getElementsByClassName('needs-validation');
//       // Loop over them and prevent submission
//       var validation = Array.prototype.filter.call(forms, function(form) {
//         form.addEventListener('submit', function(event) {
//           if (form.checkValidity() === false) {
//             event.preventDefault();
//             event.stopPropagation();
//           }
//           form.classList.add('was-validated');
//         }, false);
//       });
//     }, false);
//   })();

//////////// Progress Bar ////////////

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