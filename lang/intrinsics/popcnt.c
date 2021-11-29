#include <nmmintrin.h>
#include <stdio.h>

int
main(void)
{
	__uint64_t x = 0x1;
	//int a = _mm_popcnt_u64(x);
	__uint32_t* xx = (__uint32_t*)&x;
	int a = _mm_popcnt_u32(xx[0]) + _mm_popcnt_u32(xx[1]);
	printf("%lld %d\n", x, a);

	__uint64_t y = 0x123456789ABCDEF0;
	//int b = _mm_popcnt_u64(y);
	__uint32_t* yy = (__uint32_t*)&y;
	int b = _mm_popcnt_u32(*yy) + _mm_popcnt_u32(*(yy+1));
	printf("%lld %d\n", y, b);

	return 0;
}

// gcc -mpopcnt
