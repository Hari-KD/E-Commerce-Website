// Cart Management System
class ShoppingCart {
  constructor() {
    this.cart = this.loadCart();
    this.updateCartBadge();
  }

  // Load cart from localStorage
  loadCart() {
    const cartData = localStorage.getItem('nehaa_cart');
    return cartData ? JSON.parse(cartData) : [];
  }

  // Save cart to localStorage
  saveCart() {
    localStorage.setItem('nehaa_cart', JSON.stringify(this.cart));
    this.updateCartBadge();
  }

  // Add item to cart
  addItem(item) {
    // Check if item already exists in cart
    const existingItem = this.cart.find(cartItem => cartItem.name === item.name);
    
    if (existingItem) {
      existingItem.quantity += 1;
    } else {
      this.cart.push({
        name: item.name,
        price: item.price,
        image: item.image,
        quantity: 1
      });
    }
    
    this.saveCart();
    this.showNotification(`${item.name} added to cart!`);
  }

  // Remove item from cart
  removeItem(index) {
    this.cart.splice(index, 1);
    this.saveCart();
  }

  // Update item quantity
  updateQuantity(index, quantity) {
    if (quantity <= 0) {
      this.removeItem(index);
    } else {
      this.cart[index].quantity = quantity;
      this.saveCart();
    }
  }

  // Get cart items
  getItems() {
    return this.cart;
  }

  // Get total items count
  getTotalItems() {
    return this.cart.reduce((total, item) => total + item.quantity, 0);
  }

  // Get cart total
  getTotal() {
    return this.cart.reduce((total, item) => {
      const price = parseFloat(item.price.replace('$', ''));
      return total + (price * item.quantity);
    }, 0);
  }

  // Clear cart
  clearCart() {
    this.cart = [];
    this.saveCart();
  }

  // Update cart badge
  updateCartBadge() {
    // Disabled to prevent conflicting with Django backend cart count
    /*
    const badge = document.getElementById('cart-count');
    if (badge) {
      const count = this.getTotalItems();
      badge.textContent = count;
      badge.style.display = count > 0 ? 'flex' : 'none';
    }
    */
  }

  // Show notification
  showNotification(message) {
    // Remove existing notification if any
    const existingNotification = document.querySelector('.cart-notification');
    if (existingNotification) {
      existingNotification.remove();
    }

    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'cart-notification';
    notification.innerHTML = `
      <div class="notification-content">
        <i class="fas fa-check-circle"></i>
        <span>${message}</span>
      </div>
    `;
    
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => {
      notification.classList.add('show');
    }, 10);
    
    // Hide and remove notification after 3 seconds
    setTimeout(() => {
      notification.classList.remove('show');
      setTimeout(() => {
        notification.remove();
      }, 300);
    }, 3000);
  }
}

// Initialize cart
const cart = new ShoppingCart();

// Add to cart button handler
document.addEventListener('DOMContentLoaded', function() {
  console.log('Cart system loaded');
  
  // Update cart badge on page load
  cart.updateCartBadge();
  
  // Add to cart button on product pages
  const addToCartBtn = document.querySelector('.add-to-cart-btn');
  if (addToCartBtn) {
    console.log('Add to cart button found');
    addToCartBtn.addEventListener('click', function(e) {
      e.preventDefault();
      console.log('Add to cart clicked');
      
      try {
        const productName = document.querySelector('.product-info h1');
        const productPrice = document.querySelector('.product-info .price');
        const productImage = document.querySelector('.product-image-gallery img');
        
        if (!productName || !productPrice || !productImage) {
          console.error('Product information not found');
          return;
        }
        
        const productInfo = {
          name: productName.textContent.trim(),
          price: productPrice.textContent.trim(),
          image: productImage.src
        };
        
        console.log('Adding product:', productInfo);
        cart.addItem(productInfo);
        console.log('Cart after adding:', cart.getItems());
      } catch (error) {
        console.error('Error adding to cart:', error);
      }
    });
  } else {
    console.log('Add to cart button not found on this page');
  }
});
