
import React from 'react';

const Testimonials = () => {
  return (
    <section className='bg-gray-100 py-20'>
      <div className='container mx-auto text-center'>
        <h2 className='text-3xl font-bold mb-12'>What Our Clients Say</h2>
        <div className='carousel'>
          <div className='carousel-item bg-white p-6 rounded-lg mb-8'>
            <img src='[Photo]' alt='[Name]' className='w-24 h-24 rounded-full mx-auto mb-4'/>
            <h4 className='text-xl font-bold'>[Name]</h4>
            <p className='text-gray-600'>"The AI solutions provided by [Agency Name] have revolutionized our business processes. Highly recommend!"</p>
          </div>
          <div className='carousel-item bg-white p-6 rounded-lg mb-8'>
            <img src='[Photo]' alt='[Name]' className='w-24 h-24 rounded-full mx-auto mb-4'/>
            <h4 className='text-xl font-bold'>[Name]</h4>
            <p className='text-gray-600'>"Exceptional service and innovative solutions. We saw immediate results!"</p>
          </div>
          <div className='carousel-item bg-white p-6 rounded-lg mb-8'>
            <img src='[Photo]' alt='[Name]' className='w-24 h-24 rounded-full mx-auto mb-4'/>
            <h4 className='text-xl font-bold'>[Name]</h4>
            <p className='text-gray-600'>"Their expertise in AI is unmatched. Truly transformative for our company."</p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Testimonials;