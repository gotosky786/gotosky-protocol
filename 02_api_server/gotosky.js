(function() {
    const API_BASE = "http://127.0.0.1:8000";

    // 1. INJECT GOTOSKY 3D CSS STYLES INTO HOST WEBSITE
    const style = document.createElement('style');
    style.innerHTML = `
        #omni-floating-ad {
            position: fixed;
            bottom: 25px;
            right: 25px;
            width: 370px;
            background: #090d16;
            border-radius: 16px;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.85), 0 0 0 1px rgba(56, 189, 248, 0.35);
            overflow: hidden;
            z-index: 999999999;
            perspective: 1000px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            transition: all 0.3s ease;
        }
        .omni-media-wrapper { position: relative; width: 100%; height: 230px; background: #000; overflow: hidden; }
        #omni-ad-video { width: 100%; height: 100%; object-fit: cover; display: block; cursor: pointer; }
        #omni-3d-poster {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(180deg, rgba(9, 13, 22, 0.3) 0%, rgba(9, 13, 22, 0.95) 100%),
                        radial-gradient(circle at top right, rgba(56, 189, 248, 0.25), transparent 70%);
            display: flex; flex-direction: column; justify-content: space-between; padding: 16px;
            z-index: 5; cursor: pointer; transition: opacity 0.5s ease;
        }
        .poster-top-row { display: flex; justify-content: space-between; align-items: center; }
        .badge-3d { background: linear-gradient(135deg, #0284c7, #38bdf8); color: #000; font-size: 10px; font-weight: 800; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; }
        .rating-badge { background: rgba(0, 0, 0, 0.7); border: 1px solid rgba(255, 255, 255, 0.2); color: #facc15; font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 4px; }
        .poster-body { display: flex; flex-direction: column; gap: 6px; }
        .poster-category { font-size: 10px; color: #38bdf8; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
        .poster-title { font-size: 16px; font-weight: 800; color: #fff; line-height: 1.25; margin: 0; }
        .poster-synopsis { font-size: 11px; color: #cbd5e1; line-height: 1.4; margin: 0; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
        .omni-top-controls { position: absolute; top: 10px; right: 10px; display: flex; align-items: center; gap: 6px; z-index: 10; }
        #omni-sound-btn { background: rgba(15, 23, 42, 0.9); color: #38bdf8; border: 1px solid rgba(255, 255, 255, 0.2); padding: 5px 10px; border-radius: 6px; font-size: 12px; cursor: pointer; font-weight: 600; }
        #omni-action-btn { background: rgba(15, 23, 42, 0.9); color: #fff; padding: 5px 12px; font-size: 12px; border-radius: 6px; cursor: pointer; border: 1px solid rgba(255, 255, 255, 0.2); font-weight: 600; }
        #omni-close-x { width: 26px; height: 26px; background: rgba(15, 23, 42, 0.9); color: #94a3b8; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; font-size: 12px; border: 1px solid rgba(255, 255, 255, 0.2); }
        #omni-close-x:hover { background: #ef4444; color: #fff; }
        #omni-ad-info { padding: 12px 16px; background: #0f172a; border-top: 1px solid rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: space-between; }
        .omni-title-wrap { max-width: 220px; display: flex; flex-direction: column; gap: 2px; }
        #omni-brand-name { font-size: 13px; font-weight: 700; color: #e2e8f0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        #omni-lang-badge { font-size: 10px; color: #38bdf8; font-weight: 500; }
        #omni-cta-link { font-size: 12px; font-weight: 700; color: #38bdf8; cursor: pointer; background: rgba(56, 189, 248, 0.1); padding: 5px 10px; border-radius: 6px; border: 1px solid rgba(56, 189, 248, 0.3); text-decoration: none; }
        #omni-cta-link:hover { background: #38bdf8; color: #000; }
        @media (max-width: 600px) {
            #omni-floating-ad { top: 28% !important; bottom: auto !important; right: 12px !important; width: 230px !important; border-radius: 12px !important; }
            .omni-media-wrapper { height: 145px !important; }
            .poster-title { font-size: 12px !important; }
            .poster-synopsis { font-size: 9px !important; }
            #omni-sound-btn, #omni-action-btn { padding: 3px 8px !important; font-size: 10px !important; }
            #omni-ad-info { padding: 6px 10px !important; }
            #omni-brand-name { font-size: 11px !important; max-width: 120px !important; }
            #omni-cta-link { font-size: 10px !important; padding: 3px 7px !important; }
        }
    `;
    document.head.appendChild(style);

    // 2. CREATE AD CONTAINER
    const adContainer = document.createElement('div');
    adContainer.id = 'omni-floating-ad';
    adContainer.innerHTML = `
        <div class="omni-media-wrapper">
            <div class="omni-top-controls">
                <div id="omni-sound-btn">🔇 Unmute</div>
                <div id="omni-action-btn">--s</div>
                <div id="omni-close-x" title="Close permanently">✕</div>
            </div>
            <div id="omni-3d-poster">
                <div class="poster-top-row">
                    <span class="badge-3d" id="poster-badge">4K 3D ULTRA HD</span>
                    <span class="rating-badge" id="poster-rating">⭐ 10 / 10</span>
                </div>
                <div class="poster-body">
                    <span class="poster-category" id="poster-category">CINEMATIC ENTERTAINMENT</span>
                    <h3 class="poster-title" id="poster-title">Loading Ad...</h3>
                    <p class="poster-synopsis" id="poster-desc">Official Campaign streaming worldwide.</p>
                </div>
            </div>
            <video id="omni-ad-video" autoplay muted playsinline></video>
        </div>
        <div id="omni-ad-info">
            <div class="omni-title-wrap">
                <span id="omni-brand-name">Loading...</span>
                <span id="omni-lang-badge">Multi-Language Audio</span>
            </div>
            <span id="omni-cta-link">Visit Link ↗</span>
        </div>
    `;
    document.body.appendChild(adContainer);

    // 3. LOGIC ENGINE
    let adQueue = [];
    let currentAdIndex = 0;
    let countdownTimer = null, autoNextTimer = null, fadeTimer = null;
    let DYNAMIC_AD_DURATION = 12, timeLeft = 12, isUserUnmuted = false;

    const posterOverlay = document.getElementById('omni-3d-poster');
    const posterBadge = document.getElementById('poster-badge');
    const posterRating = document.getElementById('poster-rating');
    const posterCategory = document.getElementById('poster-category');
    const posterTitle = document.getElementById('poster-title');
    const posterDesc = document.getElementById('poster-desc');
    const actionBtn = document.getElementById('omni-action-btn');
    const soundBtn = document.getElementById('omni-sound-btn');
    const adVideo = document.getElementById('omni-ad-video');
    const brandName = document.getElementById('omni-brand-name');
    const langBadge = document.getElementById('omni-lang-badge');
    const ctaLink = document.getElementById('omni-cta-link');
    const closeX = document.getElementById('omni-close-x');

    function clearAllTimers() {
        if (countdownTimer) clearInterval(countdownTimer);
        if (autoNextTimer) clearInterval(autoNextTimer);
        if (fadeTimer) clearTimeout(fadeTimer);
    }

    async function sendTrackEvent(adId, eventType) {
        try {
            await fetch(`${API_BASE}/api/track`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ad_id: adId, event_type: eventType })
            });
        } catch(e) {}
    }

    async function fetchAds() {
        try {
            const res = await fetch(`${API_BASE}/api/ads`);
            const json = await res.json();
            if (json.ad_duration) DYNAMIC_AD_DURATION = parseInt(json.ad_duration);
            if (!json.data || json.data.length === 0 || json.total_active === 0) {
                clearAllTimers();
                adVideo.pause();
                adContainer.style.display = "none";
                return;
            }
            adContainer.style.display = "block";
            adQueue = json.data;
            loadAd(0);
        } catch(e) {}
    }

    function loadAd(index) {
        clearAllTimers();
        timeLeft = DYNAMIC_AD_DURATION;
        if (!adQueue || adQueue.length === 0) return;
        currentAdIndex = index % adQueue.length;
        const ad = adQueue[currentAdIndex];

        posterBadge.innerText = ad.badge || "4K 3D ULTRA HD";
        posterRating.innerText = ad.rating || "⭐ 10 / 10";
        posterCategory.innerText = ad.category || "CINEMATIC";
        posterTitle.innerText = ad.title || "Featured Title";
        posterDesc.innerText = ad.desc || "Official Campaign.";
        brandName.innerText = ad.title;
        langBadge.innerText = ad.lang || "English / Global Audio";

        posterOverlay.style.opacity = "1";
        adVideo.src = ad.videoUrl;
        actionBtn.innerText = timeLeft + "s";
        adVideo.muted = !isUserUnmuted;

        sendTrackEvent(ad.id, "impression");
        adVideo.currentTime = 0;
        adVideo.play().catch(() => {});

        fadeTimer = setTimeout(() => {
            if (posterOverlay) { posterOverlay.style.opacity = "0"; posterOverlay.style.pointerEvents = "none"; }
        }, 3000);

        posterOverlay.onmouseenter = () => { posterOverlay.style.opacity = "0.95"; posterOverlay.style.pointerEvents = "auto"; };
        posterOverlay.onmouseleave = () => { posterOverlay.style.opacity = "0"; posterOverlay.style.pointerEvents = "none"; };

        countdownTimer = setInterval(() => {
            timeLeft--;
            if (timeLeft > 0) {
                actionBtn.innerText = timeLeft + "s";
            } else {
                clearInterval(countdownTimer);
                let autoSec = 3;
                actionBtn.innerHTML = `Next (${autoSec}s) &#9654;&#10073;`;
                actionBtn.onclick = (e) => { e.stopPropagation(); clearAllTimers(); sendTrackEvent(ad.id, "manual_skip"); loadAd(currentAdIndex + 1); };
                autoNextTimer = setInterval(() => {
                    autoSec--;
                    if (autoSec > 0) {
                        actionBtn.innerHTML = `Next (${autoSec}s) &#9654;&#10073;`;
                    } else {
                        clearAllTimers();
                        sendTrackEvent(ad.id, "auto_skip");
                        loadAd(currentAdIndex + 1);
                    }
                }, 1000);
            }
        }, 1000);
    }

    soundBtn.onclick = (e) => {
        e.stopPropagation();
        adVideo.muted = !adVideo.muted;
        isUserUnmuted = !adVideo.muted;
        soundBtn.innerHTML = adVideo.muted ? "🔇 Unmute" : "🔊 Sound On";
    };

    function handleClick() {
        const ad = adQueue[currentAdIndex];
        sendTrackEvent(ad.id, "click");
        window.open(ad.targetUrl, '_blank');
    }

    posterOverlay.onclick = handleClick;
    adVideo.onclick = handleClick;
    ctaLink.onclick = (e) => { e.stopPropagation(); handleClick(); };

    closeX.onclick = (e) => {
        e.stopPropagation();
        clearAllTimers();
        adVideo.pause();
        adContainer.style.display = "none";
    };

    fetchAds();
})();