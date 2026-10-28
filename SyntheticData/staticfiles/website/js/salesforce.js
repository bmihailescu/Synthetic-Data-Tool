document.addEventListener('DOMContentLoaded', function () {
    var items = document.querySelectorAll('.sf-object-item');
    var bodyEl = document.body;
    var labelEl = document.getElementById('sf-object-label');
    var headingEl = document.getElementById('sf-object-heading');
    var inputEl = document.getElementById('sf-object-input');
    var headingContainer = document.getElementById('sf-heading');
    var dropdownContainer = document.getElementById('sf-dropdown-container');
    var parentActiveWrapper = document.getElementById('sf-parent-active');
    var contactParentWrapper = document.getElementById('sf-parent-wrapper');
    var contactActiveWrapper = document.getElementById('sf-active-wrapper');
    var parentInput = document.querySelector('input[name="parent_account"]');
    var activeCheckbox = document.getElementById('active');
    var optionsRow = document.getElementById('sf-options-row');
    var mandatoryListBody = document.getElementById('mandatoryFieldsListBody');
    var allFieldsListBody = document.getElementById('allFieldsListBody');
    var allFieldsRadio = document.getElementById('all_fields');
    var mandatoryRadio = document.getElementById('mandatory');
    var allFieldsLabel = document.getElementById('sf-all-fields-label');
    var allFieldsToggle = document.getElementById('sf-all-fields-toggle');
    var allStandardWrapper = document.getElementById('sf-all-standard-wrapper');
    var contactPersonWrapper = document.getElementById('sf-contact-person-wrapper');
    var contactBusinessCol = document.getElementById('sf-contact-business-col');
    var contactBothCol = document.getElementById('sf-contact-both-col');
    var contactPersonFieldsListBody = document.getElementById('contactPersonFieldsListBody');
    var contactBusinessFieldsListBody = document.getElementById('contactBusinessFieldsListBody');
    var contactBothFieldsListBody = document.getElementById('contactBothFieldsListBody');

    function isContactObject() {
        return !!(inputEl && inputEl.value === 'Contact');
    }

    function getSelectedContactAllType() {
        var selected = document.querySelector('input[name="contact_all_type"]:checked');
        return selected ? selected.value : null;
    }

    function getCurrentAccountType() {
        if (!inputEl || !inputEl.value) {
            return 'business';
        }
        if (inputEl.value === 'Account - Person') {
            return 'person';
        }
        if (inputEl.value === 'Contact') {
            return 'contact';
        }
        if (inputEl.value === 'Lead') {
            return 'lead';
        }
        // Treat all other objects (including Account - Business and any
        // not-yet-implemented objects) as business for preview purposes.
        return 'business';
    }

    function refreshContactModeUI() {
        var isContact = isContactObject();
        var currentObj = inputEl ? inputEl.value : '';

        // Update body helper classes so CSS can enforce visibility
        // rules even if inline styles are stale.
        if (bodyEl) {
            bodyEl.classList.remove('sf-contact-object', 'sf-lead-object', 'sf-person-account-object', 'sf-business-account-object');
            if (currentObj === 'Contact') {
                bodyEl.classList.add('sf-contact-object');
            } else if (currentObj === 'Lead') {
                bodyEl.classList.add('sf-lead-object');
            } else if (currentObj === 'Account - Person') {
                bodyEl.classList.add('sf-person-account-object');
            } else if (currentObj === 'Account - Business') {
                bodyEl.classList.add('sf-business-account-object');
            }
        }
        // Toggle between generic All Standard (non-Contact) and
        // Contact-specific variants (Person/Business/Both)
        if (allStandardWrapper) {
            allStandardWrapper.classList.toggle('d-none', isContact);
        }
        if (contactPersonWrapper) {
            contactPersonWrapper.classList.toggle('d-none', !isContact);
        }
        if (contactBusinessCol) {
            contactBusinessCol.classList.toggle('d-none', !isContact);
        }
        if (contactBothCol) {
            contactBothCol.classList.toggle('d-none', !isContact);
        }

        // Business Parent/Active column should only ever be visible
        // for Account - Business; hide it for all other objects.
        if (parentActiveWrapper) {
            var isBusinessAccount = (currentObj === 'Account - Business');
            if (isBusinessAccount) {
                parentActiveWrapper.classList.remove('d-none');
                parentActiveWrapper.style.display = 'flex';
            } else {
                parentActiveWrapper.classList.add('d-none');
                parentActiveWrapper.style.display = 'none';
            }
        }
    }

    function applyParentActiveLayout() {
        var obj = inputEl ? inputEl.value : '';
        var isBusinessAccount = (obj === 'Account - Business');
        var isContact = (obj === 'Contact');

        var showBusinessParent = isBusinessAccount;
        var showContactParent = false;

        if (isContact) {
            var contactType = getSelectedContactAllType();
            showContactParent = (contactType === 'business' || contactType === 'both');
        }

        var anyParent = showBusinessParent || showContactParent;

        // Business Account: only visible for Account - Business
        if (parentActiveWrapper) {
            if (showBusinessParent) {
                parentActiveWrapper.classList.remove('d-none');
                parentActiveWrapper.style.display = 'flex';
            } else {
                parentActiveWrapper.classList.add('d-none');
                parentActiveWrapper.style.display = 'none';
            }
        }

        // Contact-only Parent/Active under the middle columns
        if (contactParentWrapper) {
            if (showContactParent) {
                contactParentWrapper.classList.remove('d-none');
                contactParentWrapper.style.display = 'block';
            } else {
                contactParentWrapper.classList.add('d-none');
                contactParentWrapper.style.display = 'none';
            }
        }
        if (contactActiveWrapper) {
            if (showContactParent) {
                contactActiveWrapper.classList.remove('d-none');
                contactActiveWrapper.style.display = 'block';
            } else {
                contactActiveWrapper.classList.add('d-none');
                contactActiveWrapper.style.display = 'none';
            }
        }

        // Keep overall row horizontally centered when no parent/active visible
        if (optionsRow) {
            if (anyParent) {
                optionsRow.classList.remove('justify-content-center');
            } else {
                optionsRow.classList.add('justify-content-center');
            }
        }

        if (parentInput) {
            if (showBusinessParent) {
                parentInput.disabled = false;
            } else {
                parentInput.value = '';
                parentInput.disabled = true;
            }
        }

        if (activeCheckbox) {
            if (showBusinessParent) {
                activeCheckbox.disabled = false;
            } else {
                activeCheckbox.checked = false;
                activeCheckbox.disabled = true;
            }
        }
    }

    function updateFieldPreviews() {
        if (!window.sfFieldPreviews) {
            return;
        }
        var accountType = getCurrentAccountType();
        var previewsForType = window.sfFieldPreviews[accountType] || {};
        var mandatory = previewsForType.mandatory || [];

        if (mandatoryListBody) {
            mandatoryListBody.innerHTML = '';
            mandatory.forEach(function (name) {
                var li = document.createElement('li');
                li.textContent = name;
                mandatoryListBody.appendChild(li);
            });
        }

        if (accountType === 'contact') {
            var personAll = previewsForType.all_person || previewsForType.all || [];
            var businessAll = previewsForType.all_business || previewsForType.all || [];
            var bothAll = previewsForType.all_both || previewsForType.all || [];
            if (contactPersonFieldsListBody) {
                contactPersonFieldsListBody.innerHTML = '';
                personAll.forEach(function (name) {
                    var li = document.createElement('li');
                    li.textContent = name;
                    contactPersonFieldsListBody.appendChild(li);
                });
            }
            if (contactBusinessFieldsListBody) {
                contactBusinessFieldsListBody.innerHTML = '';
                businessAll.forEach(function (name) {
                    var li2 = document.createElement('li');
                    li2.textContent = name;
                    contactBusinessFieldsListBody.appendChild(li2);
                });
            }
            if (contactBothFieldsListBody) {
                contactBothFieldsListBody.innerHTML = '';
                bothAll.forEach(function (name) {
                    var li3 = document.createElement('li');
                    li3.textContent = name;
                    contactBothFieldsListBody.appendChild(li3);
                });
            }
        } else if (allFieldsListBody) {
            var all = previewsForType.all || [];
            allFieldsListBody.innerHTML = '';
            all.forEach(function (name) {
                var li = document.createElement('li');
                li.textContent = name;
                allFieldsListBody.appendChild(li);
            });
        }
    }

    items.forEach(function (item) {
        item.addEventListener('click', function () {
            var obj = this.getAttribute('data-object');
            if (labelEl) {
                labelEl.textContent = obj;
            }
            if (headingEl) {
                headingEl.textContent = obj;
            }
            if (inputEl) {
                inputEl.value = obj;
            }
            refreshContactModeUI();
            applyParentActiveLayout();

            // Reveal main Salesforce content after the user has chosen an object
            var mainContent = document.getElementById('sf-main-content');
            if (headingContainer) {
                headingContainer.classList.remove('d-none');
            }
            if (dropdownContainer && dropdownContainer.classList.contains('sf-dropdown-initial')) {
                dropdownContainer.classList.remove('sf-dropdown-initial');
            }
            if (mainContent && mainContent.classList.contains('d-none')) {
                mainContent.classList.remove('d-none');
            }

            updateFieldPreviews();
        });
    });

    // When Contact all-fields variant changes, ensure mode is 'all_fields'
    // and re-apply parent account visibility/layout.
    var contactAllTypeInputs = document.querySelectorAll('input[name="contact_all_type"]');
    contactAllTypeInputs.forEach(function (input) {
        input.addEventListener('change', function () {
            if (allFieldsRadio) {
                allFieldsRadio.checked = true;
            }
            if (mandatoryRadio) {
                mandatoryRadio.checked = false;
            }
            applyParentActiveLayout();
            updateFieldPreviews();
        });
    });

    if (mandatoryRadio) {
        mandatoryRadio.addEventListener('change', function () {
            // When Mandatory is selected, clear all Contact variants
            contactAllTypeInputs.forEach(function (input) {
                input.checked = false;
            });
            if (allFieldsRadio) {
                allFieldsRadio.checked = false;
            }
            applyParentActiveLayout();
            updateFieldPreviews();
        });
    }
    if (allFieldsRadio) {
        allFieldsRadio.addEventListener('change', function () {
            applyParentActiveLayout();
            updateFieldPreviews();
        });
    }

    // Initial population based on default object/mode
    refreshContactModeUI();
    applyParentActiveLayout();
    updateFieldPreviews();
});
