# by LJR
using Plots
using LaTeXStrings

fileName = ARGS

function plotFile(file::String; method::Symbol=:no, order=5)
    fit     = true
    if method == :linear
        M = 1
    elseif method == :poly
        M = 2
    elseif method == :exp
        M = 3
    elseif method == :log
        M = 4
    elseif method == :no
        fit = false
    else
        error("Method not implemented")
    end
    # Get the filename without extention name like .csv
    fileRegex = match(r"(.+?)(\.[^.]*$|$)", file)
    csv = readdlm(file, ',', Float64)
    y = csv[:, 1]; x = csv[:, 2]
    # Extent plot domain by 20%
    x_max = maximum(x)
    x_min = 0
    @show    xlen = x_max-x_min
    x_plot = 0:xlen/100:(x_max+xlen/5)
    # Plot data
    scatter(x, y, fmt = :pdf, ylabel = "Voltage (V)", xlabel = "Current (A)", label="Data")
    # Plot the best fit line
    if fit
        plot!(x_plot, dataFit(x, y, x_plot, Val{M}, order), label="Best fit line")
        savefig(fileRegex[1]*"_$method"*".pdf")
    end
    savefig(fileRegex[1]*".pdf")    
end

# Dispatch into the right argument
dataFit(x, y, x_plot, ::Type{Val{1}}, kwarg...) = dataFit(x, y, x_plot, Val{1})
dataFit(x, y, x_plot, ::Type{Val{3}}, kwarg...) = dataFit(x, y, x_plot, Val{3})
dataFit(x, y, x_plot, ::Type{Val{4}}, kwarg...) = dataFit(x, y, x_plot, Val{4})

# Linear fit by using linreg
function dataFit(x, y, x_plot, ::Type{Val{1}})
    b, a = linreg(x, y)
    map(x -> a*x + b, x_plot)
end

# Polynomial fit by QR factorization
function dataFit(x, y, x_plot, ::Type{Val{2}}, order)
    function horner(coef,x)
        sum = coef[end]
        for k = length(coef)-1:-1:1
            sum = coef[k] + x*sum
        end
        sum
    end
  A = [ float(x[i])^pow for i = 1:length(x), pow = 0:order ]
  co = A \ y
  map(x -> horner(co, x), x_plot)
end

function dataFit(x, y, x_plot, ::Type{Val{3}})
    fit = linreg(x, log(y))
    a1 = exp(fit[1]); a2 = fit[2]
    map(x -> a1*exp(x*a2), x_plot)
end

function dataFit(x, y, x_plot, ::Type{Val{4}})
    a1, a2 = linreg(log(x), y)
    map(x -> a1 + a2*log(x), x_plot)
end

plotFile.(fileName)

