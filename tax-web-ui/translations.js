// Translations for the Tax Application
const translations = {
    en: {
        // Login page
        welcome: "Welcome to TaxApp",
        enterPhone: "Please enter your phone number to access your tax account",
        phoneNumber: "Phone Number:",
        phoneNumberPlaceholder: "Enter your phone number",
        viewAccount: "View Account",
        
        // Account page
        taxAccountOverview: "Tax Account Overview",
        taxCode: "Tax Code:",
        status: "Status:",
        yearlyReturns: "Yearly Tax Returns",
        errorLoading: "Error loading",
        taxReturn: "Tax Return",
        
        // Language selector
        language: "Language",
        english: "English",
        igbo: "Igbo",
        yoruba: "Yoruba",
        hausa: "Hausa",
        
        // Alerts
        enterValidPhone: "Please enter a valid phone number",
        userNotFound: "User not found",
        failedLogin: "Failed to login: ",
        failedLoadData: "Failed to load account data: ",
        enterValidAmount: "Please enter a valid payment amount",
        paymentFailed: "Payment failed",
        paymentSuccess: "Payment processed successfully!",
        failedPayment: "Failed to process payment. Please try again later.",
        enterValidTIN: "Please enter a valid TIN (at least 6 characters)",
        regSuccess: "Registration successful! You can now login.",
        regFailed: "Registration failed: ",
        
        // Landing page
        landingTagline: "Simplified Tax Management System",
        landingDescription: "Experience a modern approach to tax management with our simplified platform. Access your tax information, make payments, and track your history through multiple interfaces designed for your convenience.",
        webAppTitle: "Web Application",
        webAppDescription: "Access your tax account through our full-featured web application. View your tax summaries, payment history, and make new payments easily from any browser.",
        mobileSimulatorTitle: "Mobile Simulator",
        mobileSimulatorDescription: "Experience how our tax management system works on mobile devices. This simulator demonstrates the SMS-based interface available for feature phones.",
        adminPanelTitle: "Admin Panel",
        adminPanelDescription: "Authorized personnel can access the administrative dashboard to manage user accounts, view tax records, and generate reports for analytical purposes.",
        launchWebApp: "Launch Web App",
        launchMobileSimulator: "Launch Mobile Simulator",
        accessAdminPanel: "Access Admin Panel",
        footerText: "© 2023 Fourier Analytics - SIMTAX Demonstration Platform",
        
        // Admin login
        adminLogin: "Admin Login",
        username: "Username:",
        password: "Password:",
        enterUsername: "Enter username",
        enterPassword: "Enter password",
        cancel: "Cancel",
        login: "Login",
        invalidCredentials: "Invalid username or password",
        
        // Account page translations
        accountLogin: "Account Login",
        enterPhoneNumber: "Enter your phone number",
        or: "or",
        createNewAccount: "Create New Account",
        registerNewAccount: "Register New Account",
        tinLabel: "TIN (Tax Identification Number):",
        enterTIN: "Enter your TIN",
        register: "Register",
        backToLogin: "Back to Login",
        taxSummary: "Tax Summary",
        currentYearSummary: "Current Year Summary",
        year: "Year",
        income: "Income",
        expenditure: "Expenditure",
        totalTaxOwed: "Total Tax Owed",
        taxOwed: "Tax Owed",
        taxPaid: "Tax Paid",
        remainingTax: "Remaining Tax",
        makePayment: "Make Payment",
        enterPaymentAmount: "Enter amount to pay",
        payNow: "Pay Now",
        taxHistory: "Tax History",
        logout: "Logout",
        
        // Status translations
        statusPending: "pending",
        statusPaid: "paid",
        statusActive: "active"
    },
    ig: {
        // Login page
        welcome: "Nno na TaxApp",
        enterPhone: "Biko tinye nọmba ekwentị gị iji banye na akaụntụ ụtụ isi gị",
        phoneNumber: "Nọmba Ekwentị:",
        phoneNumberPlaceholder: "Tinye nọmba ekwentị gị",
        viewAccount: "Lelee Akaụntụ",
        
        // Account page
        taxAccountOverview: "Nchịkọta Akaụntụ Ụtụ Isi",
        taxCode: "Koodu Ụtụ Isi:",
        status: "Ọnọdụ:",
        yearlyReturns: "Nlele Ụtụ Isi Kwa Afọ",
        errorLoading: "Nsogbu na-ebudata",
        taxReturn: "Nlele Ụtụ Isi",
        
        // Language selector
        language: "Asụsụ",
        english: "English",
        igbo: "Igbo",
        yoruba: "Yoruba",
        hausa: "Hausa",
        
        // Alerts
        enterValidPhone: "Biko tinye nọmba ekwentị dị irè",
        userNotFound: "A hụghị onye ọrụ ahụ",
        failedLogin: "Ọ gaghị enwe ike ịbanye: ",
        failedLoadData: "Ọ gaghị enwe ike ibudata data akaụntụ: ",
        enterValidAmount: "Biko tinye ego kwesịrị ekwesị",
        paymentFailed: "Ụgwọ agaghị adị irè",
        paymentSuccess: "Akwụmụgwọ arụchala nke ọma!",
        failedPayment: "Ọ gaghị enwe ike ịkwụ ụgwọ. Biko gbalịa ọzọ n'oge na-adịghị anya.",
        enterValidTIN: "Biko tinye TIN dị irè (ihe dị ka akwụkwọ 6)",
        regSuccess: "Ndebanyeaha ezutela! Ị nwere ike ịbanye ugbua.",
        regFailed: "Ndebanyeaha agaghị adị irè: ",
        
        // Landing page
        landingTagline: "Sistemụ Njikwa Ụtụ Isi Mfe",
        landingDescription: "Nwee ahụmịhe n'usoro ọhụrụ nke njikwa ụtụ isi na platformụ anyị dị mfe. Nweta ozi ụtụ isi gị, kwụọ ụgwọ, ma chọpụta akụkọ ihe gara aga site na ọtụtụ njikọ ọdịnaya emebere maka nkasi obi gị.",
        webAppTitle: "Ngwa Weebụ",
        webAppDescription: "Banye na akaụntụ ụtụ isi gị site na ngwa weebụ anyị zuru ezu. Lelee nchịkọta ụtụ isi gị, akụkọ ụgwọ, ma mee nkwụnye ụgwọ ọhụrụ site na ihe nchọgharị ọ bụla.",
        mobileSimulatorTitle: "Simulator Ekwentị",
        mobileSimulatorDescription: "Nwee ahụmịhe ka sistemụ njikwa ụtụ isi anyị si arụ ọrụ na ngwaọrụ mkpanaka. Simulator a na-egosi ọdịdị ndị dabere na SMS dị maka ekwentị atụmatụ.",
        adminPanelTitle: "Panel Nduzi",
        adminPanelDescription: "Ndị ọrụ nwere ikike ịbanye na dashboard ọchịchị iji jikwaa akaụntụ ndị ọrụ, lelee akwụkwọ ụtụ isi, ma mepụta akụkọ maka ebumnuche nyocha.",
        launchWebApp: "Malite Ngwa Weebụ",
        launchMobileSimulator: "Malite Simulator Ekwentị",
        accessAdminPanel: "Banye na Panel Nduzi",
        footerText: "© 2023 Fourier Analytics - Platformụ Ngosipụta SIMTAX",
        
        // Admin login
        adminLogin: "Mbanye Nduzi",
        username: "Aha Onye Ọrụ:",
        password: "Okwuntughe:",
        enterUsername: "Tinye aha onye ọrụ",
        enterPassword: "Tinye okwuntughe",
        cancel: "Kagbuo",
        login: "Banye",
        invalidCredentials: "Aha onye ọrụ ma ọ bụ okwuntughe adịghị mma",
        
        // Account page translations
        accountLogin: "Mbanye Akaụntụ",
        enterPhoneNumber: "Tinye nọmba ekwentị gị",
        or: "ma ọ bụ",
        createNewAccount: "Mepụta Akaụntụ Ọhụrụ",
        registerNewAccount: "Debanye Akaụntụ Ọhụrụ",
        tinLabel: "TIN (Nọmba Njirimara Ụtụ Isi):",
        enterTIN: "Tinye TIN gị",
        register: "Debanye",
        backToLogin: "Laghachi na Mbanye",
        taxSummary: "Nchịkọta Ụtụ Isi",
        currentYearSummary: "Nchịkọta Afọ Ugbu a",
        year: "Afọ",
        income: "Ego Nnata",
        expenditure: "Mgbapụ",
        totalTaxOwed: "Ụtụ Isi Enwere Ike Ikwu",
        taxOwed: "Ụtụ Isi Enwere",
        taxPaid: "Ụtụ Isi Kwụrụ",
        remainingTax: "Ụtụ Isi Fọdụrụ",
        makePayment: "Kwụọ Ụgwọ",
        enterPaymentAmount: "Tinye ego ịkwụ",
        payNow: "Kwụọ Ugbua",
        taxHistory: "Akụkọ Ụtụ Isi",
        logout: "Pụọ",
        
        // Status translations
        statusPending: "na-eche",
        statusPaid: "akwụkwọla",
        statusActive: "dị ndụ"
    },
    yo: {
        // Login page
        welcome: "E kaabo si TaxApp",
        enterPhone: "Jọwọ tẹ nọmba fonu rẹ lati wọle si account owo ori rẹ",
        phoneNumber: "Nọmba Fonu:",
        phoneNumberPlaceholder: "Tẹ nọmba fonu rẹ",
        viewAccount: "Wo Account",
        
        // Account page
        taxAccountOverview: "Akopọ Account Owo Ori",
        taxCode: "Koodu Owo Ori:",
        status: "Ipo:",
        yearlyReturns: "Ipadabọ Owo Ori ti Odun",
        errorLoading: "Asise ni gbigba",
        taxReturn: "Ipadabọ Owo Ori",
        
        // Language selector
        language: "Ede",
        english: "English",
        igbo: "Igbo",
        yoruba: "Yoruba",
        hausa: "Hausa",
        
        // Alerts
        enterValidPhone: "Jọwọ tẹ nọmba fonu to dara",
        userNotFound: "Ko ri olumulo",
        failedLogin: "Kuna lati wọle: ",
        failedLoadData: "Kuna lati gbe data wọle: ",
        enterValidAmount: "Jọwọ tẹ iye owo to dara",
        paymentFailed: "Isanwo kuna",
        paymentSuccess: "Isanwo ti pari daradara!",
        failedPayment: "Kuna lati san owo. Jọwọ gbiyanju lẹẹkansi nigbamii.",
        enterValidTIN: "Jọwọ tẹ TIN to dara (o kere ju iwe meta 6)",
        regSuccess: "Iforukọsilẹ ti pari! O le wọle bayi.",
        regFailed: "Iforukọsilẹ kuna: ",
        
        // Landing page
        landingTagline: "Eto Iṣakoso Owo Ori ti o Rọrun",
        landingDescription: "Ri iriri ọna titun fun iṣakoso owo ori pẹlu ẹrọ aiwọye wa. Wọle si alaye owo ori rẹ, ṣe awọn isanwo, ati ṣe itọpa itan rẹ nipasẹ ọpọlọpọ awọn interface ti a ṣe fun irọrun rẹ.",
        webAppTitle: "Ohun elo Wẹẹbu",
        webAppDescription: "Wọle si account owo ori rẹ nipasẹ ohun elo wẹẹbu wa to ni gbogbo awọn ẹya. Wo awọn akopọ owo ori rẹ, itan isanwo, ati ṣe awọn isanwo titun laiṣoro lati inu eyikeyi aṣawakiri.",
        mobileSimulatorTitle: "Awoṣe Fonu",
        mobileSimulatorDescription: "Ri iriri bi eto iṣakoso owo ori wa ṣe n ṣiṣẹ lori awọn ẹrọ alagbeka. Awoṣe yii ṣe afihan interface ti o da lori SMS ti o wa fun awọn fonu ẹya.",
        adminPanelTitle: "Pano Alakoso",
        adminPanelDescription: "Awọn eniyan ti o ni aṣẹ le wọle si dashboard alakoso lati ṣakoso awọn account olumulo, wo awọn iwe owo ori, ati ṣe ipilẹṣẹ awọn ijabọ fun awọn idi iṣiro.",
        launchWebApp: "Bẹrẹ Ohun elo Wẹẹbu",
        launchMobileSimulator: "Bẹrẹ Awoṣe Fonu",
        accessAdminPanel: "Wọle si Pano Alakoso",
        footerText: "© 2023 Fourier Analytics - Ẹrọ Afihan SIMTAX",
        
        // Admin login
        adminLogin: "Iwọle Alakoso",
        username: "Orukọ Olumulo:",
        password: "Ọrọigbaniwọle:",
        enterUsername: "Tẹ orukọ olumulo",
        enterPassword: "Tẹ ọrọigbaniwọle",
        cancel: "Fagilee",
        login: "Wọle",
        invalidCredentials: "Orukọ olumulo tabi ọrọigbaniwọle ko tọ",
        
        // Account page translations
        accountLogin: "Iwọle Akanti",
        enterPhoneNumber: "Tẹ nọmba fonu rẹ",
        or: "tabi",
        createNewAccount: "Ṣẹda Akanti Titun",
        registerNewAccount: "Forukọsilẹ Akanti Titun",
        tinLabel: "TIN (Nọmba Idanimọ Owo Ori):",
        enterTIN: "Tẹ TIN rẹ",
        register: "Forukọsilẹ",
        backToLogin: "Pada si Iwọle",
        taxSummary: "Akopọ Owo Ori",
        currentYearSummary: "Akopọ Odun Lọwọlọwọ",
        year: "Odun",
        income: "Owo-wiwọle",
        expenditure: "Inawo",
        totalTaxOwed: "Owo Ori Gbogbo ti a jẹ",
        taxOwed: "Owo Ori ti a jẹ",
        taxPaid: "Owo Ori ti a san",
        remainingTax: "Owo Ori ti o ku",
        makePayment: "Ṣe Isanwo",
        enterPaymentAmount: "Tẹ iye owo lati san",
        payNow: "San Bayi",
        taxHistory: "Itan Owo Ori",
        logout: "Jade",
        
        // Status translations
        statusPending: "duro",
        statusPaid: "santan",
        statusActive: "nṣiṣẹ"
    },
    ha: {
        // Login page
        welcome: "Barka da zuwa TaxApp",
        enterPhone: "Da fatan za a shigar da lambar wayar ku don samun damar shiga asusun haraji",
        phoneNumber: "Lambar Waya:",
        phoneNumberPlaceholder: "Shigar da lambar wayar ku",
        viewAccount: "Duba Asusun",
        
        // Account page
        taxAccountOverview: "Takaitaccen Bayanin Asusun Haraji",
        taxCode: "Lambar Haraji:",
        status: "Matsayi:",
        yearlyReturns: "Bayanan Haraji na Shekara-Shekara",
        errorLoading: "Kuskure yayin lodi",
        taxReturn: "Bayanan Haraji",
        
        // Language selector
        language: "Harshe",
        english: "English",
        igbo: "Igbo",
        yoruba: "Yoruba",
        hausa: "Hausa",
        
        // Alerts
        enterValidPhone: "Da fatan za a shigar da lambar waya mai inganci",
        userNotFound: "Ba a sami mai amfani ba",
        failedLogin: "An kasa shiga: ",
        failedLoadData: "An kasa load bayanai: ",
        enterValidAmount: "Da fatan za a shigar da adadin kuɗi mai kyau",
        paymentFailed: "Biyan kudin ya gaza",
        paymentSuccess: "An yi nasarar biyan kuɗi!",
        failedPayment: "An kasa biyan kuɗi. Da fatan za a sake gwadawa daga baya.",
        enterValidTIN: "Da fatan za a shigar da TIN mai kyau (a ƙalla haruffa 6)",
        regSuccess: "An yi nasarar rajista! Yanzu za ku iya shiga.",
        regFailed: "Rajista ta kasa: ",
        
        // Landing page
        landingTagline: "Tsarin Sarrafa Haraji Mai Sauƙi",
        landingDescription: "Sami ƙwarewar hanyar zamani don sarrafa haraji tare da tsarinmu mai sauƙi. Samun damar bayanan haraji, biyan kuɗi, da bibiyar tarihinku ta hanyoyi daban-daban da aka tsara don dacewa da ku.",
        webAppTitle: "Aikace-aikacen Yanar Gizo",
        webAppDescription: "Shiga asusun haraji ta hanyar aikace-aikacen yanar gizonmu cikakke. Duba taƙaitaccen bayanan haraji, tarihin biyan kuɗi, da yi sabon biyan kuɗi da sauƙi daga kowace browsers.",
        mobileSimulatorTitle: "Kwaikwayar Wayar Hannu",
        mobileSimulatorDescription: "Jin daɗin yadda tsarin sarrafa haraji ke aiki a wayoyin hannu. Wannan kwaikwayar tana nuna interface ɗin SMS da ke akwai don wayoyin hannu na musamman.",
        adminPanelTitle: "Filin Sarrafa",
        adminPanelDescription: "Jami'an da aka yarda za su iya shiga dashboard ɗin gudanarwa don sarrafa asusun masu amfani, duba bayanan haraji, da samar da rahotanni don nazarin bayanai.",
        launchWebApp: "Fara Aikace-aikacen Yanar Gizo",
        launchMobileSimulator: "Fara Kwaikwayar Wayar Hannu",
        accessAdminPanel: "Shiga Filin Sarrafa",
        footerText: "© 2023 Fourier Analytics - Dandamali na Gwaninta SIMTAX",
        
        // Admin login
        adminLogin: "Shiga na Admin",
        username: "Sunan Mai Amfani:",
        password: "Kalmar Sirri:",
        enterUsername: "Shigar da sunan mai amfani",
        enterPassword: "Shigar da kalmar sirri",
        cancel: "Soke",
        login: "Shiga",
        invalidCredentials: "Sunan mai amfani ko kalmar sirri ba daidai ba",
        
        // Account page translations
        accountLogin: "Shiga Asusun",
        enterPhoneNumber: "Shigar da lambar wayar ku",
        or: "ko",
        createNewAccount: "Ƙirƙiri Sabon Asusun",
        registerNewAccount: "Yi Rajista don Sabon Asusun",
        tinLabel: "TIN (Lambar Tantancewar Haraji):",
        enterTIN: "Shigar da TIN dinku",
        register: "Yi Rajista",
        backToLogin: "Koma Zuwa Shiga",
        taxSummary: "Taƙaitaccen Bayanan Haraji",
        currentYearSummary: "Taƙaitaccen Bayanan Shekarar Yanzu",
        year: "Shekara",
        income: "Kudin Shiga",
        expenditure: "Kudin Kashewa",
        totalTaxOwed: "Jimlar Haraji da ake Bin",
        taxOwed: "Haraji da ake Bin",
        taxPaid: "Haraji da aka Biya",
        remainingTax: "Haraji da ya Rage",
        makePayment: "Yi Biyan Kuɗi",
        enterPaymentAmount: "Shigar da adadin kuɗin da za a biya",
        payNow: "Biya Yanzu",
        taxHistory: "Tarihin Haraji",
        logout: "Fita",
        
        // Status translations
        statusPending: "jiran amincewa",
        statusPaid: "an biya",
        statusActive: "aiki"
    }
}; 