#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <time.h>

#include "evaluator_lib.c"

uint64_t rdtsc(){
    unsigned int lo,hi;
    __asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi));
    return ((uint64_t)hi << 32) | lo;
}

void benchmark() {
  unsigned int a, b, c, d, e, f, g, total=0;
  uint64_t aa, bb, cc, dd, ee, ff, gg;
  clock_t stop_time, start_time = clock();
  uint64_t stop_cycle, start_cycle = rdtsc();
  unsigned int result[32000] = {0};
  for (a = 0; a < 46; ++a) {
    aa = num_to_bit(a);
    for (b = a+1; b < 47; ++b) {
      bb = num_to_bit(b);
      for (c = b+1; c < 48; ++c) {
        cc = num_to_bit(c);
        for (d = c+1; d < 49; ++d) {
          dd = num_to_bit(d);
          for (e = d+1; e < 50; ++e) {
            ee = num_to_bit(e);
            for (f = e+1; f < 51; ++f) {
              ff = num_to_bit(f);
              for (g = f+1; g < 52; ++g) {
                gg = num_to_bit(g);
                total += 1;
                result[evaluate(aa, bb, cc, dd, ee, ff, gg)]++;
                //result[total&0x3ffu]++; // test look overhead
              }
            }
          }
        }
      }
    }
  }
  stop_cycle = rdtsc();
  stop_time = clock();
  printf("num of hands: %d\n", total);
  printf("%0.2f cycles, %0.2f nanoseconds. \n", ((double)(stop_cycle - start_cycle))/133784560.0, ((double) (stop_time - start_time)) / CLOCKS_PER_SEC / 133784560.0 * 1e9);
  unsigned int hands[9] = {0};
  unsigned int i;
  for (i=0; i<32000; i++) {
    if (i<4000) hands[0] += result[i];
    else if (i < 6147)  hands[1] += result[i];
    else if (i < 8000)  hands[2] += result[i];
    else if (i < 12000)  hands[3] += result[i];
    else if (i < 16000)  hands[4] += result[i];
    else if (i < 20000)  hands[5] += result[i];
    else if (i < 24000)  hands[6] += result[i];
    else if (i < 28000)  hands[7] += result[i];
    else hands[8] += result[i];
  }
  printf("straight flush:   %d\n", hands[8]);
  printf("four of a kind:   %d\n", hands[7]);
  printf("full house:       %d\n", hands[6]);
  printf("flush:            %d\n", hands[5]);
  printf("straight:         %d\n", hands[4]);
  printf("three of a kind:  %d\n", hands[3]);
  printf("two pair:         %d\n", hands[2]);
  printf("one pair:         %d\n", hands[1]);
  printf("no pair:          %d\n", hands[0]);
}

void test() {
  
  printf("%d\n", evaluate_cards("Ac", "Kc", "8c", "4c", "3c", "Jh", "Qh"));
  printf("%d\n", evaluate_cards("Ac", "Kc", "8c", "4c", "3c", "2c", "Qh"));
  // four of a kind
  /*
  printf("%d\n", evaluate_cards("As", "Ah", "Ad", "Ac", "Tc", "8c", "2c"));
  printf("%d\n", evaluate_cards("As", "Ah", "Ad", "Ac", "Tc", "Ts", "2c"));
  printf("%d\n", evaluate_cards("As", "Ah", "Ad", "Ac", "Kc", "Ts", "Th"));
  // full house
  printf("%d\n", evaluate_cards("As", "Ah", "Ad", "Ks", "Kc", "Js", "Th"));
  printf("%d\n", evaluate_cards("As", "Ah", "Ad", "Ks", "Kc", "Kh", "Th"));
  printf("%d\n", evaluate_cards("As", "Ah", "Ad", "Ks", "Kc", "Ts", "Th"));
  printf("%d\n", evaluate_cards("As", "Ah", "Ad", "Qs", "Qc", "Ts", "Th"));
  // straight
  printf("%d\n", evaluate_cards("As", "Ah", "Kd", "Qs", "Jc", "Ts", "Th"));
  printf("%d\n", evaluate_cards("As", "Ah", "Kd", "Qs", "Jc", "Ts", "9h"));
  printf("%d\n", evaluate_cards("As", "Ah", "2d", "3s", "4c", "5s", "9h"));
  // flush / straight flush
  printf("%d\n", evaluate_cards("As", "Ah", "Ks", "Qs", "Js", "Ts", "Th"));
  printf("%d\n", evaluate_cards("As", "Ah", "Ks", "Qs", "Js", "9s", "9h"));
  // three of a kind
  printf("%d\n", evaluate_cards("As", "Ah", "Ad", "Ks", "Ts", "9h", "8h"));
  printf("%d\n", evaluate_cards("As", "Ah", "Ad", "Qs", "Ts", "9h", "8h"));
  printf("%d\n", evaluate_cards("2s", "2h", "2d", "Ks", "Qs", "Jh", "Ah"));
  // two pair / pair
  printf("%d\n", evaluate_cards("As", "Ah", "Kd", "Ks", "Qs", "Jh", "9h"));
  printf("%d\n", evaluate_cards("2s", "2h", "3d", "3s", "As", "Kh", "Qh"));
  printf("%d\n", evaluate_cards("2s", "2h", "3d", "3s", "As", "Qh", "9h"));
  printf("%d\n", evaluate_cards("Ks", "Kh", "3d", "3s", "As", "Ah", "2h"));
  printf("%d\n", evaluate_cards("As", "Ah", "Kd", "Qs", "Ts", "8h", "9h"));
  // high card
  printf("%d\n", evaluate_cards("As", "Kd", "Qs", "Ts", "9h", "8h", "7c"));*/
}

void test_preflop() {
  clock_t stop_time, start_time = clock();
  uint64_t stop_cycle, start_cycle = rdtsc();
  float result = get_preflop_naive_strength("Ad", "Ac");
  stop_cycle = rdtsc();
  stop_time = clock();
  printf("%f\n", result);
  printf("%0.2f cycles, %0.2f seconds. \n", ((double)(stop_cycle - start_cycle)), ((double) (stop_time - start_time)) / CLOCKS_PER_SEC);
}

int main( int argc, const char* argv[]) {
  //benchmark();
  test_preflop();
  //test();
}