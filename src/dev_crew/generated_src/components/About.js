
import React from 'react';

const About = () => {
  return (
    <section className='bg-gray-100 py-20'>
      <div className='container mx-auto'>
        <h2 className='text-3xl font-bold text-center mb-12'>About Us</h2>
        <div className='text-center mb-12'>
          <p className='mb-4'>Founded in [Year], our mission has always been to empower businesses with cutting-edge AI technologies. We believe in innovation, scalability, and tailored solutions.</p>
          <p className='mb-4'>Our Mission: To provide innovative and scalable AI software solutions that drive business transformation and success.</p>
          <p className='mb-4'>Our Vision: To be the leading AI software agency recognized for our commitment to quality, innovation, and client satisfaction.</p>
        </div>
        <div className='text-center'>
          <h3 className='text-2xl font-bold mb-4'>Meet Our Team</h3>
          <div className='grid grid-cols-1 md:grid-cols-3 gap-8'>
            <div className='bg-white p-6 rounded-lg'>
              <img src='[Photo]' alt='[Name]' className='w-24 h-24 rounded-full mx-auto mb-4'/>
              <h4 className='text-xl font-bold'>[Name]</h4>
              <p className='text-gray-600'>[Title]</p>
            </div>
            <div className='bg-white p-6 rounded-lg'>
              <img src='[Photo]' alt='[Name]' className='w-24 h-24 rounded-full mx-auto mb-4'/>
              <h4 className='text-xl font-bold'>[Name]</h4>
              <p className='text-gray-600'>[Title]</p>
            </div>
            <div className='bg-white p-6 rounded-lg'>
              <img src='[Photo]' alt='[Name]' className='w-24 h-24 rounded-full mx-auto mb-4'/>
              <h4 className='text-xl font-bold'>[Name]</h4>
              <p className='text-gray-600'>[Title]</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default About;