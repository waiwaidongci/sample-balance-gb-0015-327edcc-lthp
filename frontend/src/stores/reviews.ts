import{reactive}from 'vue';import{getReviews}from '../api/reviews';import type{Review}from '../types/domain';
export const reviews=reactive({items:[]as Review[]});export async function loadReviews(){reviews.items=await getReviews();}
