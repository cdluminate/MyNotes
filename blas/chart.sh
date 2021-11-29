f="chart.m"
nsizes=7
nbench=10
echo "%!/usr/bin/octave" > $f
echo "" >> $f
echo "sz = [" >> $f
cat result | sed -e 's/[()]//g' | awk '!/GEMM/{print $1}' >> $f
echo "];" >> $f
echo "sz = log2(reshape(sz, $nsizes, $nbench));" >> $f
echo "" >> $f
echo "tm = [" >> $f
cat result | sed -e 's/[()]//g' | awk '!/GEMM/{print $2}' >> $f
echo "];" >> $f
echo "tm = log2(reshape(tm, $nsizes, $nbench));" >> $f
echo "" >> $f
echo "gf = [" >> $f
cat result | sed -e 's/[()]//g' | awk '!/GEMM/{print $4}' >> $f
echo "];" >> $f
echo "gf = reshape(gf, $nsizes, $nbench);" >> $f
echo "" >> $f
echo "tags = [" >> $f
cat result | awk '/GEMM/{print "\"" $0 "\""}' \
	| sed -e 's/Benchmark//g' | sed -e 's/_/ /g' >> $f
echo "];" >> $f
echo "" >> $f
echo "plot(sz, tm, 'x-'); grid on;" >> $f
echo "xlabel('log2(size)'); ylabel('log2(microsec)');" >> $f
echo "legend(tags, 'Location', 'northwest');" >> $f
echo "print -dsvg tm.svg;" >> $f
echo "" >> $f
echo "plot(sz, gf, 'x-'); grid on;" >> $f
echo "xlabel('log2(size)'); ylabel('gflops');" >> $f
echo "legend(tags, 'Location', 'northeast');" >> $f
echo "print -dsvg gf.svg;" >> $f
