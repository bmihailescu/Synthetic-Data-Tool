const savedSchemaSelect = document.querySelector("#saved-schema-select")

if (savedSchemaSelect) {
    const storageKey = "syntheticData.savedSchemas"
    const schemaNameInput = document.querySelector("#saved-schema-name")
    const saveSchemaButton = document.querySelector("#save-schema-button")
    const deleteSchemaButton = document.querySelector("#delete-schema-button")
    const schemaPreview = document.querySelector("#saved-schema-preview")
    const schemaStatus = document.querySelector("#saved-schema-status")
    let savedSchemas = []
    let storageReady = true

    function showStatus(message) {
        schemaStatus.textContent = message
    }

    function getColumnFormat(row, dataType) {
        const formatContainer = row.querySelector("#placeholderDiv")

        if (dataType === "Number") {
            const numberInputs = formatContainer.querySelectorAll('input[type="number"]')
            return `${numberInputs[0].value},${numberInputs[1].value}`
        }

        if (dataType === "Date") {
            const dateInputs = formatContainer.querySelectorAll('input[type="date"]')
            const formatSelect = formatContainer.querySelector("select")
            return `${formatSelect.value},${dateInputs[0].value},${dateInputs[1].value}`
        }

        const formatInput = formatContainer.querySelector('[name="format_option"]')
        return formatInput ? formatInput.value : ""
    }

    function getCurrentColumns() {
        return Array.from(document.querySelector("#manual-schema-fields").children)
            .filter(row => row.id && row.id.startsWith("row"))
            .map(row => {
                const dataTypeInput = row.querySelector('[name="data_type"]')
                const dataType = dataTypeInput.value.replace(/ /g, "_")
                return {
                    name: row.querySelector('[name="column_name"]').value.trim(),
                    dataType,
                    format: getColumnFormat(row, dataType),
                    blankPercent: row.querySelector('[name="blankPercent"]').value,
                    specialCharacters: row.querySelector('[name="badData"]').value
                }
            })
    }

    function hasValidColumnInputs(row) {
        return Array.from(row.querySelectorAll("input, select, textarea"))
            .every(control => control.checkValidity())
    }

    function renderPreview(schema) {
        schemaPreview.textContent = ""
        if (!schema) {
            return
        }

        const table = document.createElement("table")
        table.className = "table table-sm table-bordered"
        const header = table.createTHead().insertRow()
        ;["Column", "Data Type", "Format", "Blank (%)", "Special Characters"].forEach(label => {
            const cell = document.createElement("th")
            cell.scope = "col"
            cell.textContent = label
            header.appendChild(cell)
        })

        const body = table.createTBody()
        schema.columns.forEach(column => {
            const row = body.insertRow()
            const typeLabel = column.dataType.replace(/_/g, " ")
            ;[column.name, typeLabel, column.format || "(empty)", column.blankPercent, column.specialCharacters]
                .forEach(value => {
                    row.insertCell().textContent = value
                })
        })
        schemaPreview.appendChild(table)
    }

    function renderSchemaOptions(selectedId = "") {
        savedSchemaSelect.replaceChildren(new Option("Select a saved schema", ""))
        savedSchemas.forEach(schema => {
            savedSchemaSelect.add(new Option(schema.name, schema.id))
        })
        savedSchemaSelect.value = selectedId
        deleteSchemaButton.disabled = !selectedId
    }

    function persistSchemas() {
        try {
            localStorage.setItem(storageKey, JSON.stringify(savedSchemas))
            return true
        } catch (error) {
            showStatus(`Could not save schemas in this browser: ${error.message}`)
            return false
        }
    }

    function applyColumnFormat(row, column) {
        const formatContainer = row.querySelector("#placeholderDiv")
        const parts = column.format.split(",")

        if (column.dataType === "Number") {
            const numberInputs = formatContainer.querySelectorAll('input[type="number"]')
            numberInputs[0].value = parts[0] || ""
            numberInputs[1].value = parts[1] || ""
            return
        }

        if (column.dataType === "Date") {
            const dateInputs = formatContainer.querySelectorAll('input[type="date"]')
            formatContainer.querySelector("select").value = parts[0] || ""
            dateInputs[0].value = parts[1] || ""
            dateInputs[1].value = parts[2] || ""
            return
        }

        const formatInput = formatContainer.querySelector('[name="format_option"]')
        if (formatInput) {
            formatInput.value = column.format
        }
    }

    function loadSchema(schema) {
        if (schema.columns.some(column => !attr_list.includes(column.dataType))) {
            throw new Error("The saved schema contains an unsupported data type.")
        }

        const schemaMode = document.querySelector("#schema_mode")
        schemaMode.value = "manual"
        schemaMode.dispatchEvent(new Event("change"))

        const manualFields = document.querySelector("#manual-schema-fields")
        Array.from(manualFields.children)
            .filter(row => row.id && row.id.startsWith("row"))
            .forEach(row => row.remove())

        schema.columns.forEach(column => {
            const row = newRow()
            row.querySelector('[name="column_name"]').value = column.name

            const dataTypeLink = Array.from(row.querySelectorAll("[data-data-type]"))
                .find(link => link.dataset.dataType === column.dataType)
            if (!dataTypeLink) {
                throw new Error(`Unsupported saved data type: ${column.dataType}`)
            }
            dataTypeLink.click()
            applyColumnFormat(row, column)
            row.querySelector('[name="blankPercent"]').value = column.blankPercent
            row.querySelector('[name="badData"]').value = column.specialCharacters
        })
    }

    function validSchemaList(value) {
        return Array.isArray(value) && value.every(schema =>
            schema &&
            typeof schema.id === "string" &&
            typeof schema.name === "string" &&
            Array.isArray(schema.columns) &&
            schema.columns.every(column =>
                column &&
                typeof column.name === "string" &&
                typeof column.dataType === "string" &&
                typeof column.format === "string" &&
                typeof column.blankPercent === "string" &&
                typeof column.specialCharacters === "string"
            )
        )
    }

    try {
        const storedSchemas = localStorage.getItem(storageKey)
        if (storedSchemas) {
            const parsedSchemas = JSON.parse(storedSchemas)
            if (!validSchemaList(parsedSchemas)) {
                throw new Error("Saved schema data has an invalid format.")
            }
            savedSchemas = parsedSchemas
        }
        renderSchemaOptions()
    } catch (error) {
        storageReady = false
        saveSchemaButton.disabled = true
        showStatus(`Could not load saved schemas from this browser: ${error.message}`)
    }

    savedSchemaSelect.addEventListener("change", () => {
        const schema = savedSchemas.find(item => item.id === savedSchemaSelect.value)
        renderPreview(schema)
        if (schema) {
            try {
                loadSchema(schema)
                schemaNameInput.value = schema.name
                showStatus(`Loaded "${schema.name}" into the manual schema editor.`)
            } catch (error) {
                showStatus(`Could not load this schema: ${error.message}`)
            }
        } else {
            schemaNameInput.value = ""
            showStatus("")
        }
    })

    saveSchemaButton.addEventListener("click", () => {
        if (!storageReady) {
            return
        }

        try {
            const name = schemaNameInput.value.trim()
            if (!name) {
                showStatus("Enter a name for this schema.")
                schemaNameInput.focus()
                return
            }

            const columns = getCurrentColumns()
            const rows = Array.from(document.querySelector("#manual-schema-fields").children)
                .filter(row => row.id && row.id.startsWith("row"))
            if (!columns.length || columns.some(column => !column.name || !column.dataType) ||
                rows.some(row => !hasValidColumnInputs(row))) {
                showStatus("Add and complete at least one column before saving.")
                return
            }

            if (savedSchemas.some(schema => schema.name.toLowerCase() === name.toLowerCase())) {
                showStatus("A saved schema with that name already exists.")
                return
            }

            const schema = {
                id: `${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`,
                name,
                columns
            }
            savedSchemas.push(schema)
            if (!persistSchemas()) {
                savedSchemas.pop()
                return
            }

            renderSchemaOptions(schema.id)
            renderPreview(schema)
            showStatus(`Saved "${name}" in this browser.`)
        } catch (error) {
            showStatus(`Could not save schema: ${error.message}`)
        }
    })

    deleteSchemaButton.addEventListener("click", () => {
        if (!storageReady || !savedSchemaSelect.value) {
            return
        }

        const schemaIndex = savedSchemas.findIndex(schema => schema.id === savedSchemaSelect.value)
        if (schemaIndex === -1) {
            return
        }

        const [deletedSchema] = savedSchemas.splice(schemaIndex, 1)
        if (!persistSchemas()) {
            savedSchemas.splice(schemaIndex, 0, deletedSchema)
            return
        }

        renderSchemaOptions()
        renderPreview(null)
        schemaNameInput.value = ""
        showStatus(`Deleted "${deletedSchema.name}".`)
    })
}
