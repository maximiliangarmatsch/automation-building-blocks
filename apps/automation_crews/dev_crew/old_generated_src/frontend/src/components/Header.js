import React from 'react';

function Header() {
  return (
    <header className='bg-white shadow-md py-4'>
      <div className='container mx-auto flex justify-between items-center'>
        <div className='text-2xl font-bold text-blue-600'>AI Software Agency</div>
        <nav className='space-x-4'>
          <a href='#home' className='text-gray-600 hover:text-blue-600'>Home</a>
          <a href='#about' className='text-gray-600 hover:text-blue-600'>About Us</a>
          <a href='#services' className='text-gray-600 hover:text-blue-600'>Services</a>
          <a href='#case-studies' className='text-gray-600 hover:text-blue-600'>Case Studies</a>
          <a href='#blog' className='text-gray-600 hover:text-blue-600'>Blog</a>
          <a href='#contact' className='text-gray-600 hover:text-blue-600'>Contact</a>
          <a href='#get-started' className='bg-blue-600 text-white px-4 py-2 rounded'>Get Started</a>
        </nav>
      </div>
    </header>
  );
}

export default Header;
