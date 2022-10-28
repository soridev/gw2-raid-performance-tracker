var newGuild = false;

function initUI() {
    function initGuildDropdown() {
        axios.get(restAPIUrl + "guilds/").then(function (response) {
            let data = response.data;
            let guildDropdown = document.getElementById("guild-dropdown-body");

            for (let i = 0; i < data.length; i++) {
                let guildItem = `<li><a class="dropdown-item guild-item" href="#">${data[i].guild_name}</a></li>`;
                guildDropdown.innerHTML += guildItem;
            }

            $(".guild-item").click(function () {
                let guildName = $(this).text();

                axios.get(restAPIUrl + "guild-members/" + guildName + "/").then(function (response) {
                    let data = response.data;
                    let guildMembers = "";

                    for (let i = 0; i < data.length; i++) {

                        if (i === data.length - 1) {
                            guildMembers += `${data[i].account_name}`;
                        }
                        else {
                            guildMembers += `${data[i].account_name}\n`;
                        }
                    }

                    // assign values to input fields
                    $("#i-guild-name").val(guildName);
                    $("#guild-account-names").val(guildMembers);
                    $("#guild-config-body").show();

                    $("#guild-account-names").height(0);
                    $("#guild-account-names").height($("#guild-account-names")[0].scrollHeight);
                });
            });
        });
    }

    function init() {
        initGuildDropdown();
    }
    init();
}

function expandTextarea(id) {
    document.getElementById(id).addEventListener('keyup', function () {
        this.style.overflow = 'hidden';
        this.style.height = 0;
        this.style.height = this.scrollHeight + 'px';
    }, false);
}

window.onload = function () {
    initUI();
    expandTextarea('guild-account-names');
}
