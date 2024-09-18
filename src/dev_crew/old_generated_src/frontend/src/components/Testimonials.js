import React from 'react';

function Testimonials() {
  return (
    <section id='testimonials' className='py-20'>
      <div className='container mx-auto text-center'>
        <h2 className='text-3xl font-bold mb-10'>What Our Clients Say</h2>
        <div className='carousel'>
          <div className='carousel-item'>
            <div className='p-6 bg-white rounded-lg shadow-lg'>
              <img src='https://picsum.photos/id/237/200/300' alt='Client 1' className='w-16 h-16 rounded-full mx-auto mb-4' />
              <p className='text-gray-600 mb-2'>"Their AI solutions have revolutionized our operations and boosted our productivity."</p>
              <p className='font-bold'>John Doe</p>
              <p className='text-gray-600'>CEO, Tech Innovators</p>
            </div>
          </div>
          <div className='carousel-item'>
            <div className='p-6 bg-white rounded-lg shadow-lg'>
              <img src='https://picsum.photos/id/237/200/300' alt='Client 2' className='w-16 h-16 rounded-full mx-auto mb-4' />
              <p className='text-gray-600 mb-2'>"The team is highly knowledgeable and their solutions are top-notch."</p>
              <p className='font-bold'>Jane Smith</p>
              <p className='text-gray-600'>CTO, Smart Solutions Inc.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Testimonials;
