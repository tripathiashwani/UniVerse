<template>
  <div>
    <form @submit.prevent="handlePayment">
      <div class="form-group">
        <label for="email">Email</label>
        <input
          type="email"
          v-model="email"
          id="email"
          class="form-control"
          required
          placeholder="Enter your email"
        />
      </div>
      <div id="card-element" class="form-group"></div>
      <button type="submit" class="btn btn-primary">Pay</button>
    </form>
  </div>
</template>

<script>
import { loadStripe } from '@stripe/stripe-js';
import axios from 'axios';

export default {
  name: 'Payment',
  data() {
    return {
      stripe: null,
      cardElement: null,
      email: "", 
    };
  },
  async mounted() {
    this.stripe = await loadStripe(
      "pk_test_51Q1CyGRx5Jd1fk6eUV5anPkUj9vIgxi0n3vhbMR66NKrvo6V0XFpRJIkSArM1t2KFbh6iwDOmuBlYqd57OJiLJL600NnT6qAuA"
    );
    const elements = this.stripe.elements();
    this.cardElement = elements.create("card");
    this.cardElement.mount("#card-element");
  },
  methods: {
    async handlePayment() {
    try {
      const { data } = await axios.post("/api/payment/", {
        email: this.email, 
        amount: 1,  
      });
      console.log("Payment data: ", data.url);
      const  clientSecret  = data.url;
      console.log("Client secret: ", clientSecret);

       
       window.location.href=clientSecret
      
    } catch (error) {
      console.error("Error processing payment: ", error);
    }
  },
  },
};
</script>
<style scoped>
.form-group {
  margin-bottom: 20px;
}
</style>
