function dtheta = oscillator(t,theta,w0,N,KN)

dtheta = zeros(N,N);
theta = reshape(theta,N,N);

for i = 1:N %row
    for j = 1:N %col
    
        theta_diff = -theta(i,j) + theta; % follow paper eqn 11
        
        % i was talking self thru this loop, i may have gotten backward but
        % testing to see
        % Compute distance matrix D at (i,j)
        a = i*ones(1,N); %one row many cols
        % Dx = repmat(abs((1:N) - a),N,1); % all ints to N minus row i val repeat for each row to N
        Dx = repmat(abs((1:N) - j*ones(1,N)),N,1); % all ints to N minus col j val repeat for each row to N

        b = j*ones(N,1); %one col many rows
        % Dy = repmat(abs((1:N)' - b),1,N); % all ints to N minus col j val repeat for each col to N
        Dy = repmat(abs((1:N)' - i*ones(N,1)),1,N); % all ints to N minus row i val repeat for each col to N
        
        D = sqrt(Dx.^2 + Dy.^2);
        
        % Set Gaussian Wavelet 
%         W = KN/sqrt(2*pi*1)*exp(-1/2 * D.^2 );
        
        % Morlet wavelet
        W = KN*exp(-D.^2/2).*cos(D);
        dtheta(i,j) = w0(i,j) + sum(W.*sin(theta_diff), 'all');
        
    end
end
dtheta = reshape(dtheta,N^2,1);
end
