import React from 'react';

function Contact() {
  return (
    <section id='contact' className='py-20'>
      <div className='container mx-auto flex flex-col md:flex-row items-center'>
        <div className='w-full md:w-1/2 mb-10 md:mb-0'>
          <form className='bg-white p-8 rounded-lg shadow-lg'>
            <h2 className='text-3xl font-bold mb-6'>Contact Us</h2>
            <div className='mb-4'>
              <label className='block text-gray-700 mb-2' htmlFor='name'>Your Name</label>
              <input type='text' id='name' className='w-full px-4 py-2 border rounded-lg' placeholder='Your Name' />
            </div>
            <div className='mb-4'>
              <label className='block text-gray-700 mb-2' htmlFor='email'>Your Email</label>
              <input type='email' id='email' className='w-full px-4 py-2 border rounded-lg' placeholder='Your Email' />
            </div>
            <div className='mb-4'>
              <label className='block text-gray-700 mb-2' htmlFor='message'>Your Message</label>
              <textarea id='message' className='w-full px-4 py-2 border rounded-lg' rows='4' placeholder='Your Message'></textarea>
            </div>
            <button type='submit' className='bg-blue-600 text-white px-4 py-2 rounded'>Submit</button>
          </form>
        </div>
        <div className='w-full md:w-1/2 md:pl-10'>
          <h2 className='text-3xl font-bold mb-4'>Contact Information</h2>
          <p className='mb-4'><strong>Address:</strong> 123 AI Lane, Innovation City, Techland</p>
          <p className='mb-4'><strong>Phone:</strong> +123 456 7890</p>
          <p className='mb-4'><strong>Email:</strong> contact@aisoftwareagency.com</p>
        </div>
      </div>
    </section>
  );
}

export default Contact;
