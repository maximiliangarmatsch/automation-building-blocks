
import React from 'react';

const Contact = () => {
  return (
    <section className='bg-white py-20'>
      <div className='container mx-auto text-center'>
        <h2 className='text-3xl font-bold mb-12'>Get in Touch</h2>
        <form className='max-w-lg mx-auto'>
          <div className='mb-4'>
            <input type='text' placeholder='Name' className='w-full p-3 border border-gray-300 rounded'/>
          </div>
          <div className='mb-4'>
            <input type='email' placeholder='Email' className='w-full p-3 border border-gray-300 rounded'/>
          </div>
          <div className='mb-4'>
            <input type='tel' placeholder='Phone Number' className='w-full p-3 border border-gray-300 rounded'/>
          </div>
          <div className='mb-4'>
            <textarea placeholder='Message' className='w-full p-3 border border-gray-300 rounded' rows='4'></textarea>
          </div>
          <button type='submit' className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'>
            Send Message
          </button>
        </form>
      </div>
    </section>
  );
}

export default Contact;