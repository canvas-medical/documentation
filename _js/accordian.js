const toggles = document.querySelectorAll(".accordion");
let i;

for (i = 0; i < toggles.length; i++) {
    toggles[i].addEventListener("click",  function() {
        this.classList.toggle("active");
            if (this.classList.contains('active')){
                console.log("HAs Class")
                this.innerHTML="X Hide child Attributes"
                this.parentElement.style.border="2px solid #f5f5f5";
                this.style.display="block";
            } else {
                this.innerHTML="Show child Attributes"
                this.parentElement.style.border="0px solid #f5f5f5";
                this.style.display="inline-block";
            }
        var panel = this.nextElementSibling;
        if (panel.style.display === "block") {
            panel.style.display = "none";
        } else {
            panel.style.display = "block";
        }
    });

    // toggles[i].addEventListener("click", toggleAccord);

}
