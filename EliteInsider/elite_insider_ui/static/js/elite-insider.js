function checkGuildCookie() {
    if(Cookies.get("ei_selected_guild") === undefined){
        fetchUrl = restAPIUrl + "user-guilds/";
        axios.get(fetchUrl).then(function (response) {
            let data = response.data;

            if (data.length > 1){
                for (let i = 0; i < data.length; i++) {
                    $(".modal-body").append(data[i].guild_name);
                }
    
                openGuildSelectionModal();
            }
            else{
                Cookies.set("ei_selected_guild", data[0].guild_name);
            }
        })
        .catch(function (error) {
            if(error.response.data.status_code === 404){
                Cookies.set("ei_selected_guild", "none-configured");
            }
        });
    }
}

function openGuildSelectionModal() {
    let modalOptions = {keyboard: true, focus:true, backdrop: 'static'}
    let guildSelectorModal = new bootstrap.Modal(document.getElementById('guild-selector-modal'), modalOptions);
    guildSelectorModal.show();
}

document.addEventListener("DOMContentLoaded", function(event) {
   
    const showNavbar = (toggleId, navId, bodyId, headerId) =>{
        const toggle = document.getElementById(toggleId),
        nav = document.getElementById(navId),
        bodypd = document.getElementById(bodyId),
        headerpd = document.getElementById(headerId)
        
        // Validate that all variables exist
        if(toggle && nav && bodypd && headerpd){
            toggle.addEventListener('click', ()=>{
            // show navbar
            nav.classList.toggle('navbar-show');
            // change icon
            toggle.classList.toggle('bx-x');
            // add padding to body
            bodypd.classList.toggle('body-pd');
            // add padding to header
            headerpd.classList.toggle('body-pd');
            });
        }
    }
    
    showNavbar('header-toggle','nav-bar','body-pd','header');
    
    /*===== LINK ACTIVE =====*/
    const linkColor = document.querySelectorAll('.nav_link');
    
    function colorLink(){
        if(linkColor){
            linkColor.forEach(l=> l.classList.remove('active'));
            this.classList.add('active');
        }
    }
    
    linkColor.forEach(l=> l.addEventListener('click', colorLink));
    
    // check if guild cookie is set for user, else open modal to select it.
    checkGuildCookie();
});