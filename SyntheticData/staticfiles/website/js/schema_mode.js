const schemaMode = document.querySelector("#schema_mode")
const v6SchemaMode = document.querySelector("#v6_schema_mode")
const avivaSchemaMode = document.querySelector("#aviva_schema_mode")

if (schemaMode) {
    function updateSchemaMode() {
        const manualMode = schemaMode.value === "manual"
        const v6Mode = schemaMode.value === "data_analytics" && v6SchemaMode.value === "v6_bike"
        const avivaMode = schemaMode.value === "api_tests" && avivaSchemaMode.value === "aviva_integration"

        document.querySelectorAll("[data-manual-schema]").forEach(section => {
            section.hidden = !manualMode
            section.querySelectorAll("input, select, button").forEach(control => {
                control.disabled = !manualMode
            })
        })

        document.querySelectorAll("[data-data-analytics-schema]").forEach(section => {
            section.hidden = schemaMode.value !== "data_analytics"
            section.querySelectorAll("input, select, button").forEach(control => {
                control.disabled = schemaMode.value !== "data_analytics"
            })
        })

        document.querySelectorAll("[data-api-tests-schema]").forEach(section => {
            section.hidden = schemaMode.value !== "api_tests"
            section.querySelectorAll("input, select, button").forEach(control => {
                control.disabled = schemaMode.value !== "api_tests"
            })
        })

        document.querySelectorAll("[data-v6-only]").forEach(section => {
            section.hidden = !v6Mode
            section.querySelectorAll("input, select, button").forEach(control => {
                control.disabled = !v6Mode
            })
        })

        document.querySelectorAll("[data-aviva-only]").forEach(section => {
            section.hidden = !avivaMode
        })

        const countInput = document.querySelector("#num_of_entries")
        countInput.placeholder = avivaMode ? "Files per type" : "No. of Records"
        countInput.setAttribute("aria-label", avivaMode ? "Files per type" : "Number of records")

        document.querySelector("#v6-json-only").hidden = !v6Mode
    }

    schemaMode.addEventListener("change", updateSchemaMode)
    v6SchemaMode.addEventListener("change", updateSchemaMode)
    avivaSchemaMode.addEventListener("change", updateSchemaMode)
    updateSchemaMode()
}