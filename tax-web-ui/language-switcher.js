// Language Switcher Functionality

// Initialize with English as default language
let currentLanguage = localStorage.getItem('taxAppLanguage') || 'en';

// Function to update the UI with the selected language
function updateLanguage(lang) {
    // Save the selected language in localStorage for persistence
    localStorage.setItem('taxAppLanguage', lang);
    currentLanguage = lang;
    
    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[lang] && translations[lang][key]) {
            element.textContent = translations[lang][key];
        }
    });
    
    // Update placeholders for inputs with data-i18n-placeholder attribute
    document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
        const key = element.getAttribute('data-i18n-placeholder');
        if (translations[lang] && translations[lang][key]) {
            element.placeholder = translations[lang][key];
        }
    });
    
    // Update the language dropdown to show the current language
    const languageSelector = document.getElementById('languageSelector');
    if (languageSelector) {
        languageSelector.value = lang;
    }
}

// Function to create and insert the language selector
function createLanguageSelector() {
    // Check if a language selector already exists to prevent duplicates
    if (document.getElementById('languageSelector')) {
        return; // Exit if a language selector already exists
    }
    
    const languageContainer = document.createElement('div');
    languageContainer.className = 'language-selector-container';
    
    const label = document.createElement('label');
    label.setAttribute('for', 'languageSelector');
    label.setAttribute('data-i18n', 'language');
    label.textContent = translations[currentLanguage].language;
    
    const select = document.createElement('select');
    select.id = 'languageSelector';
    select.className = 'language-selector';
    
    // Add language options
    const languages = [
        { code: 'en', name: 'english' },
        { code: 'ig', name: 'igbo' },
        { code: 'yo', name: 'yoruba' },
        { code: 'ha', name: 'hausa' }
    ];
    
    languages.forEach(lang => {
        const option = document.createElement('option');
        option.value = lang.code;
        option.setAttribute('data-i18n', lang.name);
        option.textContent = translations[currentLanguage][lang.name];
        if (lang.code === currentLanguage) {
            option.selected = true;
        }
        select.appendChild(option);
    });
    
    // Add change event listener
    select.addEventListener('change', function() {
        updateLanguage(this.value);
    });
    
    languageContainer.appendChild(label);
    languageContainer.appendChild(select);
    
    // Add the language selector to the page
    const container = document.querySelector('.container');
    if (container) {
        // Insert at the top of the container
        container.insertBefore(languageContainer, container.firstChild);
    }
}

// Initialize language on page load
document.addEventListener('DOMContentLoaded', function() {
    // Add data-i18n attributes to all elements that need translation
    initializeI18nAttributes();
    
    // Create the language selector
    createLanguageSelector();
    
    // Apply the current language
    updateLanguage(currentLanguage);
});

// Function to initialize data-i18n attributes on elements
function initializeI18nAttributes() {
    // Set attributes on the login page
    if (document.getElementById('loginForm')) {
        // Login page elements
        document.querySelector('h1').setAttribute('data-i18n', 'welcome');
        document.querySelector('p').setAttribute('data-i18n', 'enterPhone');
        document.querySelector('label[for="phoneNumber"]').setAttribute('data-i18n', 'phoneNumber');
        document.getElementById('phoneNumber').setAttribute('data-i18n-placeholder', 'phoneNumberPlaceholder');
        document.querySelector('button[type="submit"]').setAttribute('data-i18n', 'viewAccount');
    }
    
    // Set attributes on the account page
    if (document.querySelector('.user-info')) {
        // Account page title
        document.querySelector('title').textContent = translations[currentLanguage].taxAccountOverview;
        
        // Tax code and status labels
        const labels = document.querySelectorAll('.info-label');
        if (labels.length >= 2) {
            labels[0].setAttribute('data-i18n', 'phoneNumber');
            labels[1].setAttribute('data-i18n', 'taxCode');
            labels[2].setAttribute('data-i18n', 'status');
        }
        
        // Returns section
        const returnsSectionTitle = document.querySelector('#yearlyReturns').previousElementSibling;
        if (returnsSectionTitle) {
            returnsSectionTitle.setAttribute('data-i18n', 'yearlyReturns');
        }
    }
} 