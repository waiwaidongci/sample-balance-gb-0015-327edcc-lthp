import{request}from './client';import type{Review,Audit}from '../types/domain';
export const getReviews=()=>request<Review[]>('/reviews');
export const createReview=(data:unknown)=>request<Review>('/reviews',{method:'POST',body:JSON.stringify(data)});
export const getAudits=()=>request<Audit[]>('/audits');
