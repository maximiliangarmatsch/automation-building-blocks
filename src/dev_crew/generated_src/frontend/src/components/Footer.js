import React from 'react';

function Footer() {
  return (
    <footer className='bg-gray-800 text-white py-10'>
      <div className='container mx-auto grid grid-cols-1 md:grid-cols-4 gap-8'>
        <div>
          <div className='text-2xl font-bold mb-4'>AI Software Agency</div>
          <p>Innovating with Intelligence</p>
        </div>
        <div>
          <h3 className='text-xl font-bold mb-4'>Navigation</h3>
          <ul>
            <li><a href='#home' className='hover:underline'>Home</a></li>
            <li><a href='#about' className='hover:underline'>About Us</a></li>
            <li><a href='#services' className='hover:underline'>Services</a></li>
            <li><a href='#case-studies' className='hover:underline'>Case Studies</a></li>
            <li><a href='#blog' className='hover:underline'>Blog</a></li>
            <li><a href='#contact' className='hover:underline'>Contact</a></li>
          </ul>
        </div>
        <div>
          <h3 className='text-xl font-bold mb-4'>Follow Us</h3>
          <div className='space-x-4'>
            <a href='https://facebook.com' className='hover:underline'>Facebook</a>
            <a href='https://twitter.com' className='hover:underline'>Twitter</a>
            <a href='https://linkedin.com' className='hover:underline'>LinkedIn</a>
            <a href='https://instagram.com' className='hover:underline'>Instagram</a>
          </div>
        </div>
        <div>
          <h3 className='text-xl font-bold mb-4'>Newsletter</h3>
          <form>
            <input type='email' placeholder='Your Email' className='w-full px-4 py-2 mb-4 border rounded-lg' />
            <button type='submit' className='bg-blue-600 text-white px-4 py-2 rounded'>Subscribe</button>
          </form>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
