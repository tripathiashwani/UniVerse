<template>
     <div class="space-y-4 ">
            <div>go to profile and chat </div>
            <PeopleYouMayKnow />
          </div>
</template>

<script>

import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue';

export default {
  name: 'MessagesView',
  components: {
    PeopleYouMayKnow,
  }
  
    
  
}
</script>