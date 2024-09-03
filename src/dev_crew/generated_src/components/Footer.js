
import React from 'react';

const Footer = () => {
  return (
    <footer className='bg-gray-800 text-white py-8'>
      <div className='container mx-auto text-center'>
        <div className='mb-4'>
          <a href='#home' className='mx-2 hover:underline'>Home</a>
          <a href='#services' className='mx-2 hover:underline'>Services</a>
          <a href='#about' className='mx-2 hover:underline'>About Us</a>
          <a href='#case-studies' className='mx-2 hover:underline'>Case Studies</a>
          <a href='#contact' className='mx-2 hover:underline'>Contact</a>
        </div>
        <div className='mb-4'>
          <a href='https://facebook.com' className='mx-2' target='_blank' rel='noopener noreferrer'>
            <img src='facebook-icon.png' alt='Facebook' className='inline w-6'/>
          </a>
          <a href='https://twitter.com' className='mx-2' target='_blank' rel='noopener noreferrer'>
            <img src='twitter-icon.png' alt='Twitter' className='inline w-6'/>
          </a>
          <a href='https://linkedin.com' className='mx-2' target='_blank' rel='noopener noreferrer'>
            <img src='linkedin-icon.png' alt='LinkedIn' className='inline w-6'/>
          </a>
          <a href='https://instagram.com' className='mx-2' target='_blank' rel='noopener noreferrer'>
            <img src='instagram-icon.png' alt='Instagram' className='inline w-6'/>
          </a>
        </div>
        <div>
          <p>Contact Information:</p>
          <p>Email: <a href='mailto:your-email@example.com' className='underline'>your-email@example.com</a></p>
          <p>Phone: <a href='tel:your-phone-number' className='underline'>Your Phone Number</a></p>
          <p>Address: Your Address</p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;