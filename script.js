const siteData = {
    socials: {
        instagram: {
            label: "Instagram",
            handle: "@Shirokinstudio",
            url: "https://www.instagram.com/shirokinstudio/",
            count: 413
        },
        youtubeDev: {
            label: "YouTube Dev",
            handle: "@Shirokinstudio",
            url: "https://www.youtube.com/@ShiroKinStudio",
            count: 63
        },
        youtubeLol: {
            label: "LoL Rehber",
            handle: "@ShiroxKin",
            url: "https://www.youtube.com/@ShiroxKin",
            count: 2500
        },
        tiktok: {
            label: "TikTok",
            handle: "@Shirokinstudio",
            url: "https://www.tiktok.com/@shirokinstudio",
            count: 16
        }
    },
    games: {
        guildMaster: {
            url: "https://play.google.com/store/apps/details?id=com.shirokinstudio.guildmaster",
            buttonText: "Play Store'a Git"
        },
        area81: {
            url: "https://play.google.com/store/apps/details?id=com.shirokinstudio.area81",
            buttonText: "Play Store'a Git"
        }
    },

    contact: {
        email: "Shirokinstudio@gmail.com"
    }
};

function formatFollowerCount(value) {
    const number = Number(value);

    if (Number.isNaN(number)) return "0";

    if (number < 1000) {
        return String(number);
    }

    if (number < 1000000) {
        const formatted = number / 1000;
        return `${formatted.toFixed(1).replace(".0", "")}K`;
    }

    const formatted = number / 1000000;
    return `${formatted.toFixed(1).replace(".0", "")}M`;
}

function applySocialData() {
    document.querySelectorAll("[data-social]").forEach(card => {
        const key = card.dataset.social;
        const social = siteData.socials[key];

        if (!social) return;

        const name = card.querySelector(".social-name");
        const handle = card.querySelector(".social-handle");
        const count = card.querySelector(".social-count");

        card.href = social.url;
        card.target = "_blank";

        if (name) name.textContent = social.label;
        if (handle) handle.textContent = social.handle;
        if (count) count.textContent = formatFollowerCount(social.count);
    });
}

function applyGameLinks() {
    const guildButton = document.querySelector("[data-game-link='guildMaster']");
    const areaButton = document.querySelector("[data-game-link='area81']");
    const guildDetailCard = document.querySelector("[data-game-detail='guildMaster']");
    const areaDetailCard = document.querySelector("[data-game-detail='area81']");

    if (guildButton) {
        const guildUrl = siteData.games.guildMaster.url;

        if (guildUrl) {
            guildButton.href = guildUrl;
            guildButton.target = "_blank";
            guildButton.classList.remove("store-cta-disabled");
            guildButton.classList.add("store-cta-blue");
            guildButton.querySelector("span").textContent = siteData.games.guildMaster.buttonText || "Play Store'a Git";
        } else {
            guildButton.href = "javascript:void(0)";
            guildButton.removeAttribute("target");
            guildButton.classList.add("store-cta-disabled");
            guildButton.classList.remove("store-cta-blue");
            guildButton.querySelector("span").textContent = "Yakinda";
        }
    }

    if (areaButton) {
        areaButton.href = siteData.games.area81.url;
        areaButton.target = "_blank";
        areaButton.querySelector("span").textContent = siteData.games.area81.buttonText;
    }

    if (guildDetailCard) {
        const guildUrl = siteData.games.guildMaster.url;
        guildDetailCard.href = guildUrl || "javascript:void(0)";
        if (guildUrl) guildDetailCard.target = "_blank";
    }

    if (areaDetailCard) {
        areaDetailCard.href = siteData.games.area81.url;
        areaDetailCard.target = "_blank";
    }
}

function applyContactData() {
    const mail = document.querySelector(".contact-mail");

    if (!mail) return;

    mail.textContent = siteData.contact.email;
    mail.href = `mailto:${siteData.contact.email}`;
}

applySocialData();
applyGameLinks();
applyContactData();

console.log("ShiroKin Studio site loaded.");
