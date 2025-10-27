function initiateGPay() {
    // GPay integration (use a payment gateway API like Razorpay or Stripe with GPay option)
    alert("Redirecting to GPay payment...");
    // Example: window.location.href = 'gpay-payment-link';
}

// Prevent screenshots
document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
});

document.addEventListener('keydown', function(e) {
    if (e.key === 'PrintScreen' || (e.ctrlKey && e.key === 'p')) {
        e.preventDefault();
        alert('Screenshots are disabled for security.');
    }
});