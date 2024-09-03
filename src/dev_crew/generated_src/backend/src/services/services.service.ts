import { Injectable } from '@nestjs/common';

@Injectable()
export class ServicesService {
  private readonly services = [];

  findAll() {
    return this.services;
  }

  create(service: any) {
    this.services.push(service);
    return service;
  }

  findOne(id: string) {
    return this.services.find(service => service.id === id);
  }

  update(id: string, updateServiceDto: any) {
    const existingService = this.findOne(id);
    if (existingService) {
      Object.assign(existingService, updateServiceDto);
    }
    return existingService;
  }

  remove(id: string) {
    const index = this.services.findIndex(service => service.id === id);
    if (index >= 0) {
      return this.services.splice(index, 1);
    }
  }
}