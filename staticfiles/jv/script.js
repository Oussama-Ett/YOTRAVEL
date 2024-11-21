function annulerFormulaire() {
    /*document.getElementById("myForm").reset();*/
    alert("Erreur!");
}

function validerFormulaire() {
    // Vous pouvez ajouter ici le code pour traiter les données du formulaire
    alert("Formulaire validé ! ");
}
function previewImage() {
    var input = document.getElementById('imageInput');
    var preview = document.getElementById('imagePreview');

    // Vérifier si un fichier a été sélectionné
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        // Lorsque le fichier est chargé, afficher l'aperçu
        reader.onload = function(e) {
            preview.innerHTML = '<img src="' + e.target.result + '" alt="Image Preview">';
        };

        // Charger le fichier en tant que données URL
        reader.readAsDataURL(input.files[0]);
    }
}
