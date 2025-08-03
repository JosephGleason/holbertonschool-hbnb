document.addEventListener('DOMContentLoaded', () => {
  if (window.location.pathname.endsWith('add_review.html')) {
    const token = getCookie('token');
    if (!token) {
      // not logged in → back to index
      window.location.href = 'index.html';
      return;  // stop any further script on this page
    }
  }
  checkAuthentication();
    // === Additional logic for place.html ===
  if (window.location.pathname.endsWith('place.html')) {
    const placeId = new URLSearchParams(window.location.search).get('id');
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');

    if (!token) {
      if (addReviewSection) addReviewSection.style.display = 'none';
    } else {
      if (addReviewSection) addReviewSection.style.display = 'block';
      // Make the “Add a Review” link include the place ID
      const reviewLink = addReviewSection.querySelector('a');
      if (reviewLink) {
        reviewLink.href = `add_review.html?id=${placeId}`;
      }

      if (placeId) fetchPlaceDetails(token, placeId);
    }
  }

  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
          document.cookie = `token=${data.access_token}; path=/; max-age=86400`;
          window.location.href = 'index.html';
        } else {
          alert(data.message || 'Login failed. Check your credentials.');
        }
      } catch (error) {
        console.error('Network error:', error);
        alert('Network error. Please try again later.');
      }
    });
  }
  
  const reviewForm = document.getElementById('review-form');
if (reviewForm) {
  reviewForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const token = getCookie('token');
    if (!token) {
      alert('You must be logged in to submit a review.');
      return;
    }

    const placeId = new URLSearchParams(window.location.search).get('id');
    const comment = document.getElementById('review').value;
    const rating  = document.getElementById('rating').value;

    try {
      // ← Updated fetch call:
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/reviews/place/${placeId}/new`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            text: comment,               // use "text" not "comment"
            rating: parseInt(rating, 10)
          })
        }
      );

      if (response.ok) {
        alert('Review submitted!');
        window.location.href = `place.html?id=${placeId}`;
      } else {
        const data = await response.json();
        alert(data.error || 'Failed to submit review');
      }
    } catch (error) {
      console.error('Error submitting review:', error);
      alert('Error submitting review.');
    }
  });
}

  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    // Add options
    ['10', '50', '100', 'All'].forEach(function (val) {
      const option = document.createElement('option');
      option.value = val;
      option.textContent = val;
      priceFilter.appendChild(option);
    });

    // Add filtering logic
    priceFilter.addEventListener('change', (event) => {
      const selectedPrice = event.target.value;
      const cards = document.querySelectorAll('.place-card');

      cards.forEach(function (card) {
        const priceText = card.querySelector('p').textContent;
        const match = priceText.match(/\$(\d+)/);
        const price = match ? parseInt(match[1]) : 0;

        if (selectedPrice === 'All' || price <= parseInt(selectedPrice)) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    });
  }
});

function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [key, value] = cookie.trim().split('=');
    if (key === name) return value;
  }
  return null;
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (loginLink) {
    if (!token) {
      loginLink.style.display = 'inline-block';
    } else {
      loginLink.style.display = 'none';
      fetchPlaces(token);
    }
  }
}

async function fetchPlaces(token) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch places');
    }

    const places = await response.json();
    displayPlaces(places);
  } catch (error) {
    console.error('Error fetching places:', error);
  }
}

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  if (!placesList) return;
  placesList.innerHTML = '';

  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';

    card.innerHTML = `
      <h2>${place.title}</h2>
      <p>Price: $${place.price}/night</p>
      <p>${place.description}</p>
      <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
    `;

    placesList.appendChild(card);
  });
}

async function fetchPlaceDetails(token, placeId) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch place details');
    }

    const place = await response.json();
    displayPlaceDetails(place);

    fetchPlaceReviews(token, placeId);

  } catch (error) {
    console.error('Error fetching place details:', error);
    const container = document.getElementById('place-details');
    if (container) container.innerHTML = '<p>Error loading place details.</p>';
  }
}

function displayPlaceDetails(place) {
  const container = document.getElementById('place-details');
  if (!container) return;

  container.innerHTML = `
    <div class="place-info">
      <h2>${place.title}</h2>
      <p><strong>Host:</strong> ${place.host || 'N/A'}</p>
      <p><strong>Price:</strong> $${place.price}/night</p>
      <p><strong>Description:</strong> ${place.description}</p>
      ${
        place.amenities && place.amenities.length > 0
          ? `<ul>${place.amenities.map(a => `<li>${a}</li>`).join('')}</ul>`
          : ''
      }
    </div>
  `;
}

async function fetchPlaceReviews(token, placeId) {
  try {
    const response = await fetch(
      `http://127.0.0.1:5000/api/v1/reviews/place/${placeId}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    if (!response.ok) {
      throw new Error('Failed to fetch reviews');
    }
    const reviews = await response.json();
    displayReviews(reviews);
  } catch (error) {
    console.error('Error fetching reviews:', error);
  }
}

function displayReviews(reviews) {
  const reviewsSection = document.getElementById('reviews');
  if (!reviewsSection) return;

  // Clear any static content or loading indicators
  reviewsSection.innerHTML = '<h2>Reviews</h2>';

  if (reviews.length === 0) {
    reviewsSection.innerHTML += '<p>No reviews yet.</p>';
    return;
  }

  reviews.forEach(review => {
    const card = document.createElement('div');
    card.className = 'review-card';

    const stars = '⭐'.repeat(review.rating || 0);

    card.innerHTML = `
      <p><strong>${review.user_id || 'Anonymous'}</strong>: "${review.text}"</p>
      <p>Rating: ${stars}</p>
    `;

    reviewsSection.appendChild(card);
  });
}
