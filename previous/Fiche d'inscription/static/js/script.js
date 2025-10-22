console.log("JS chargé !");

const optdept = {
    "GINFO" : [
        "II",
        "TIC",
    ],
    "GEL" : [
        "ET",
        "TE",
        "EN",
        "ET"
    ],
    "GCI": [
            "BTP",
            "IS",
            "GT"
    ],
    "GME": [
            "CM",
            "FM",
            "MA"
    ],
    "GFO": [
            "EF",
            "MB",
            "IB"
    ],
    "ESF": [
            "PGAV",
            "ESCOCO",
            "NHD"
    ],
    "STEG": [
            "CF",
            "Marketing",
            "Économie"
    ],
    "ITH": ["ITH"],
    "TAD": ["CAO"],
    "SE": ["CO"],
    "GCH": ["CI"],
    "ESB": ["IM"]
};

document.getElementById('departement').addEventListener('change', function() {
    const dept = this.value;
    const optsel = document.getElementById('option');

    optsel.innerHTML = '<option value="" disabled selected>Choisissez une option</option>';; 
    if (optdept[dept]){
        optdept[dept].forEach(opt => {
            const option = document.createElement('option');
            option.value = opt;
            option.textContent = opt;
            optsel.appendChild(option);
        });
    }
    console.log(optdept["GINFO"]);
    console.log(optdept[dept]);
});