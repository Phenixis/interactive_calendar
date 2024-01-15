const elements = document.getElementsByClassName("element");

for (let pas = 0; pas < elements.length; pas++) {
    var element = elements.item(pas)
    var events = element.getElementsByClassName("name").item(0);
    var input = events.children.item(1);
    var submit = events.children.item(2);
    
    input.addEventListener('change', (event) => {
        if (event.target.value != "") {
            addEventToEventsList(event);
            event.target.value = "";
        }
    }, false);
};

function addEventToEventsList(event) {
    var newLi = document.createElement("li");
    var newElt = document.createElement("input");
    
    newElt.classList.add("event");
    newElt.setAttribute("type", "text");
    newElt.setAttribute("value", event.target.value);
    
    newLi.appendChild(newElt);
    
    event.target.parentElement.getElementsByTagName("ul").item(0).appendChild(newLi);
}