let row_num = 0


function newRow() {

    function deleteRow(e) {
        row = e.target.id
        document.getElementById("row" + row ).remove();
    }

    row_num += 1

    //Create div.row
    const div = document.createElement('div');
    div.className = 'd-flex row-hl'//'row align-items-center';
    div.id = "row" + row_num

    //Create minus button
    const minus = document.createElement('button')
    minus.type = "button";
    minus.className = "btn btn-secondary";
    minus.textContent = "-"
    minus.addEventListener('click',deleteRow);
    minus.id = row_num;
    div.appendChild(minus);

    //create input
    const input = document.createElement('input')
    input.className = "form-control col-2"
    input.placeholder = "Input"
    input.type = "text"
    input.name = "column_name"
    input.required = true

    //////Create Dropdown//////
    const ul = document.createElement('ul')
    ul.className = "nav nav-pills col-2"
    ul.id = "DataTypeDropdown"

    const li = document.createElement('li')
    li.className = "nav-item dropdown"
    li.innerHTML = '<a class="nav-link dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false" id="dataTypeDisplayValue" name="dataTypeDisplayValue">Dropdown</a> '
    ul.appendChild(li)

    //Hidden input - for post request 
    const hiddenDataTypeInput = document.createElement('input')
    hiddenDataTypeInput.className = "text-center"
    hiddenDataTypeInput.name = "data_type"
    hiddenDataTypeInput.style = "height: 0px; font-size: 0; margin: 0 0 1px; display:block; float:middle; margin-left: auto; margin-right: auto ;opacity:0" //; 
    hiddenDataTypeInput.required = true
    li.appendChild(hiddenDataTypeInput);

    //Div for Data Type List
    const divDataType = document.createElement("div")
    divDataType.className = "dropdown-menu"
    divDataType.id ="divDataTypeList"
    divDataType.style = ""

    ////Data Type List//////
    function dropdownValue(e){
        this.parentElement.parentElement.firstChild.text = this.text
        this.parentElement.parentElement.firstChild.nextElementSibling.value = this.text
    }

    attr_list.forEach(attr => {
        const a = document.createElement("a")
        a.className="dropdown-item"
        a.href="#/"
        a.innerHTML=attr.replace("_"," ")
        
        a.addEventListener('click',dropdownValue);
        a.addEventListener('click',function format(e) {
            const currentRowFormat = this.parentElement.parentElement.parentElement.nextElementSibling
            currentRowFormat.textContent = ""
            if (attr == "Multiple_Choice") {
                currentRowFormat.innerHTML = '<input class="form-control" placeholder="Eg. red,blue,green" type="text" name="format_option" required>'                
            }
            else if (attr == "Text") {
                currentRowFormat.innerHTML = '<input class="form-control" placeholder="No. of Words (optional)" type="number" min="1" name="format_option">'                
            }
            else if (attr == "String") {
                currentRowFormat.innerHTML = '<input class="form-control" placeholder="Length" type="number" name="format_option" min="1" required>'                
            }
            else if (attr == "Number") {
                currentRowFormat.innerHTML = `  <div class="d-flex flex-row row-hl">   
                                                    <input class="form-control col-4" placeholder="Min" type="number" required>
                                                    <input class="form-control col-4" placeholder="Max" type="number" required>
                                                    <input id="numberFormat" name="format_option" type="hidden">      
                                                </div>          
                `          
            }
            else if (attr == "Name") {
                currentRowFormat.innerHTML = `
                <select class="custom-select" name="format_option">
                    <option value="fullName">Full Name</option>
                    <option value="firstName">First Name</option>
                    <option value="lastName">Last Name</option>
                <select>
                `   
            }
            else if (attr == "Address") {
                currentRowFormat.innerHTML = `
                <select class="custom-select" name="format_option">
                    <option value="fullAddress">Full Address</option>
                    <option value="addressLine1">Address Line 1</option>
                    <option value="addressLine2">Address Line 2</option>
                    <option value="county">County</option>
                    <option value="postcode">Postcode</option>
                </select>
            `
            }
            else if (attr == "Date") {
                currentRowFormat.innerHTML =  `
                <div class="d-flex flex-row row-hl">
                    <div class="px-1 item-hl"> <div class="align-baseline">Start</div> <div class="align-top p-1">End</div>
                    </div>
                    <div class="px-1 item-hl"> <div class="align-baseline"><input class="" type= "date" required></div> <div class="align-top"><input class="" type= "date" required></div>  
                    </div>
                    <div class="px-1 item-hl col-5"> <div class="text-center">Date Format</div>
                        <select class="custom-select">
                            <option value="%d/%m/%Y">dd/mm/yyyy</option>
                            <option value="%d/%m/%Y %H:%M:%S">dd/mm/yyyy hh:mm:ss</option>
                            <option value="%d-%m-%Y">dd-mm-yyyy</option>
                            <option value="%Y-%m-%d">yyyy-mm-dd</option>
                            <option value="%Y-%m-%dT%H:%M:%SZ">ISO 8601 UTC</option>
                            <option value="%m/%d/%Y">mm/dd/yyyy</option>
                        </select> 
                    </div>
                    <input id="dateFormat" name="format_option" type="hidden"> 
                </div>`       
            }
                        
        });


        divDataType.appendChild(a);    
    });

    li.appendChild(divDataType)

    // Placeholder Div - Format Column
    const placeholderDiv = document.createElement("div")
    placeholderDiv.id = "placeholderDiv"
    placeholderDiv.className = "col-4 px-0"

    //Blank Values
    const blankDiv = document.createElement("div")
    blankDiv.id = "blankDiv"
    blankDiv.className = "px-2 col-1"
    const blankInput = document.createElement("input")
    blankInput.className = "form-control"
    blankInput.type = "number"
    blankInput.name = "blankPercent"
    blankInput.id = "BlankCheckBox"
    blankInput.min = 0
    blankInput.max = 100
    blankInput.maxLength = 2
    blankInput.value = 0
    blankInput.required = true
    blankDiv.appendChild(blankInput)

    // Bad Data Slider
    const badDataDiv = document.createElement("div")
    badDataDiv.className = "px-3"
    badDataDiv.innerHTML = '<input class="custom-range mt-2" type="range" min="0" max="4" step="1" value="0" name="badData"></input>' 
    

    //Put input and drop down into div row
    div.appendChild(input)
    div.appendChild(ul)
    div.appendChild(placeholderDiv)
    div.appendChild(blankDiv)
    div.appendChild(badDataDiv)

    //put div.row into div.container
    const add = document.querySelector("#add");
    document.querySelector("form.container").insertBefore(div,add);
}

document.querySelector("#add button").addEventListener('click',newRow)


newRow();






