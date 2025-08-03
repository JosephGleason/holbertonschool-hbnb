// ===== scripts.js =====

// 1) Utility: read a cookie
function getCookie(name) {
  const pairs = document.cookie.split(';').map(c => c.trim().split('='));
  for (const [key, val] of pairs) {
    if (key === name) return val;
  }
  return null;
}

// 2) FETCHERS & RENDERS

// Fetch and render the list of places (index.html)
async function fetchPlaces() {
  const token = getCookie('token');
  const res = await fetch('http://127.0.0.1:5000/api/v1/places/', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch places');
  const places = await res.json();
  displayPlaces(places);
}

// Render place cards into #places-list
function displayPlaces(places) {
  const container = document.getElementById('places-list');
  if (!container) return;
  container.innerHTML = '';

  // image URLs mapped by title
  const imagesByPlaceTitle = {
  "Casa del Sol": "images/casadelsol.png",
  "Ocean View Retreat": "images/oceanviewretreat.png",
  "Rainforest Cabin": "images/rainforestcabin.png"
};


  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';
    // set price for filtering
    card.dataset.price = place.price;

    const imageUrl = imagesByPlaceTitle[place.title] || 'images/default.png';

    card.innerHTML = `
      <img src="${imageUrl}" alt="${place.title}" class="place-img">
      <h3>${place.title}</h3>
      <p>Price: $${place.price}</p>
      <a class="details-button" href="place.html?id=${place.id}">View Details</a>
    `;
    container.appendChild(card);
  });
}

// Fetch and render a single place’s details (place.html)
async function fetchPlaceDetails(placeId) {
  const token = getCookie('token');
  const res = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch place details');
  const place = await res.json();
  displayPlaceDetails(place);
}

// Render detailed info + add-review link + reviews
function displayPlaceDetails(place) {
  const container = document.getElementById('place-details');
  if (!container) return;

  // Set banner image
  const banner = document.getElementById('banner-img');
  const bannerImages = {
    "Casa del Sol": "images/casadelsol.png",
    "Ocean View Retreat": "images/oceanviewretreat.png",
    "Rainforest Cabin": "images/rainforestcabin.png"
  };
  
  banner.src = bannerImages[place.title] || "images/default.png";
  banner.alt = place.title;
  container.innerHTML = `
    <h2>${place.title}</h2>
    <p>${place.description}</p>
    <p><strong>Price:</strong> $${place.price}</p>
    <p><strong>Amenities:</strong> ${place.amenities.map(a => a.name).join(', ')}</p>
  `;
  const token = getCookie('token');
  const addSection = document.getElementById('add-review');
  if (addSection) {
    addSection.style.display = token ? 'block' : 'none';
    if (token) addSection.querySelector('a').href = `add_review.html?id=${place.id}`;
  }
  fetchReviews(place.id);
}

// Fetch & render reviews for a place
async function fetchReviews(placeId) {
  const token = getCookie('token');
  const res = await fetch(
    `http://127.0.0.1:5000/api/v1/reviews/place/${placeId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    }
  );
  if (!res.ok) throw new Error('Failed to fetch reviews');
  const reviews = await res.json();
  displayReviews(reviews);
}
function displayReviews(reviews) {
  const container = document.getElementById('reviews');
  if (!container) return;
  container.innerHTML = reviews.length
    ? reviews.map(r => `
        <div class="review-card">
          <p>${r.text}</p>
          <p><em>By ${r.user_id} — Rating: ${r.rating}/5</em></p>
        </div>
      `).join('')
    : '<p>No reviews yet.</p>';
}

// Submit a new review (add_review.html)
async function submitReview(placeId, text, rating) {
  const token = getCookie('token');
  const res = await fetch(
    `http://127.0.0.1:5000/api/v1/reviews/place/${placeId}/new`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ text, rating: Number(rating) })
    }
  );
  return res;
}

// 3) DOMContentLoaded: wire up per‑page logic

document.addEventListener('DOMContentLoaded', () => {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  if (loginLink) loginLink.style.display = token ? 'none' : 'inline-block';

  // LOGIN PAGE
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async e => {
      e.preventDefault();
      const email = loginForm.email.value;
      const pass  = loginForm.password.value;
      const res = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type':'application/json' },
        body: JSON.stringify({ email, password: pass })
      });
      const json = await res.json();
      if (res.ok) {
        document.cookie = `token=${json.access_token}; path=/; max-age=86400`;
        window.location.href = 'index.html';
      } else {
        alert(json.error || json.message || 'Login failed');
      }
    });
    return;
  }

  // INDEX PAGE
  if (window.location.pathname.endsWith('index.html')) {
    const filter = document.getElementById('price-filter');
    if (filter) {
      filter.addEventListener('change', () => {
        const max = filter.value === 'all' ? Infinity : Number(filter.value);
        document.querySelectorAll('.place-card').forEach(c => {
          c.style.display = Number(c.dataset.price) <= max ? '' : 'none';
        });
      });
    }
    fetchPlaces().catch(e => console.error(e));
    return;
  }

  // PLACE DETAILS
  if (window.location.pathname.endsWith('place.html')) {
    const id = new URLSearchParams(location.search).get('id');
    if (!token) {
      const add = document.getElementById('add-review');
      if (add) add.style.display = 'none';
    }
    if (id) fetchPlaceDetails(id).catch(e => console.error(e));
    return;
  }

  // ADD REVIEW
  if (window.location.pathname.endsWith('add_review.html')) {
    if (!token) return void (window.location.href = 'index.html');
    const id = new URLSearchParams(location.search).get('id');
    const form = document.getElementById('review-form');
    if (form) {
      form.addEventListener('submit', async e => {
        e.preventDefault();
        const text   = form.review.value.trim();
        const rating = form.rating.value;
        console.log('🔍 Submitting Review', { id, text, rating });

        const res = await submitReview(id, text, rating);
        if (res.ok) {
          alert('Review posted');
          location.href = `place.html?id=${id}`;
        } else {
          const j = await res.json();
          alert(j.error || 'Failed to submit');
        }
      });
    }
  }
});

