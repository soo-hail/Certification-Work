function openTab(tabName){
    var tabs = document.getElementsByClassName("tab-links");
    var tabContaints = document.getElementsByClassName("tab-containts");

    // FIRST REMOVE DEFAULT-CONTENT(ACTIVE-LINK AND ACTIVE-TAB).
    for(tablink of tabs){
        tablink.classList.remove("active-link"); // REMOVING CLASS-NAME
    }

    for(tabContaint of tabContaints){
        tabContaint.classList.remove("active-tab"); // REMOVING CLASS-NAME
    }

    // DISPLAY DESIRED-TAB.
    event.currentTarget.classList.add("active-link"); // ADD CLASS-NAME TO THE ELEMENT.
    document.getElementById(tabName).classList.add("active-tab"); //// ADD CLASS-NAME TO THE ELEMENT.

}
