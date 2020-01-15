document.addEventListener("DOMContentLoaded", function(){



//     document.getElementById("submitBtn").onclick = function() {
//     this.disabled = true;
// }


    var submitBtn = document.querySelector("#submitBtn")


    submitBtn.addEventListener("submit", function (event) {
        this.style.display = 'none';

    })


    });
