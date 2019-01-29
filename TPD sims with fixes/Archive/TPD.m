function []=TPD()
screen=get(0,'screensize');
screen=screen(3:4);

handle.figure=figure(...
    'Name', 'TPD Simulator',...
    'NumberTitle', 'off',...
    'color',[.94,.94,.94],...
    'position',[0*screen(1),0.02*screen(2),screen(1),0.9*screen(2)]);
%Axes
handle.axes=axes(...
    'units','normalized',...
    'position',[0.36,0.5,0.38,0.45]);
handle.axes2=axes(...
    'units','normalized',...
    'position',[0.36,0.10,0.38,0.3]);
handle.parameters=uipanel(...
    'Title', 'Parameters',...
    'backgroundcolor',[.94,.94,.94],...
    'position', [0.76,0.31,0.23,0.65]);
%Table
columnname={'Temp [K]','100%','75%','50%','25%'};
columnformat={'numeric','numeric','numeric','numeric','numeric'};
handle.table=uitable(...
    'units','normalized',...
    'position', [0.039 0.11 0.25 0.3],...
    'ColumnName', columnname,...
    'ColumnFormat', columnformat,...
    'RowName', []);
columnformat2={'numeric','numeric','numeric','numeric'};
columnname2={'100%','75%','50%','25%'};
handle.table2=uitable(...
    'units','normalized',...
    'position',[0.76, 0.09,0.23, 0.08],...
    'columnname',columnname2,...
    'columnformat',columnformat2,...
    'rowname',[]);
uicontrol(...
    'style','text',...
    'units','normalized',...
    'string','Maximum T for various Coverages [K]',...
    'position',[0.76,0.17,0.23,0.02]);
uicontrol(...
    'style', 'text',...
    'units', 'normalized',...
    'string', 'Desorption Signal Data [K vs molecules/(cm^2*s)]',...
    'position', [0.06,0.41,0.2,0.025]);
uicontrol(...
    'style', 'text',...
    'units','normalized',...
    'string','Use initial and final T to change x axis after you have run the program',...
    'fontsize',8,...
    'parent',handle.parameters,...
    'position',[0.05,0.56,0.9,0.1]);
%--------------------------------------------------------------------------
% %axes for figure
% % imageArray= imread('C:\Users\Caitlin Danger Allen\Desktop\tpd\tpd2.jpg')
% % handle.axesimage=axes(...
% %     'units','normalized',...
% %     'position',[0.0125,0.5,0.3,0.6]);
% % axes(handle.axesimage)
% % imshow(imageArray)
%--------------------------------------------------------------------------
%strings with equations
textbox
    function []=textbox()
        handle.newtextbox=axes(...
            'units','normalized',...
            'position',[0.0125,0.46,0.3,0.52],...
            'xtick',[], 'ytick', [],...
            'xcolor', 'w', 'ycolor','w');
        str(1)={'==Temperature Programmed Desorption=='};
        str(2)= {'Rate of desorption from unit surface area:'};
        str(3)={'$$N(t)=-\frac{d \sigma}{d t}=v_n \sigma^n exp(-\frac{E-A \sigma} {RT})$$'};
        str(4)={''};
        str(5)={'With linear temperature change:'};
        str(6)={'$$T = T_o + \beta t$$'};
        str(7)={''};
        str(8)={'The rate of desorption is then:'};
        str(9)={'$$N(T)=-\frac{d \sigma}{d T}=\frac{v_n \sigma^n}{\beta} exp(-\frac{E-A \sigma}{RT})$$'};
        str(10)={''};
        str(11)={'$$N(t) = $$  desorption rate [$molecules/(cm^2*s$)]'};
        str(12)={'$$\sigma = $$ surface coverage [$molecules/cm^2$]'};
        str(13)={'$$v_n = $$ pre exponential'};
        str(14)={'$$\beta = $$ rate of temperature change [$K/s$]'};
        str(15)={'$$E = $$ activation energy [$kcal/mol$]'};
        str(16)={'$$A = $$ energy coverage dependence'};
        str(17)={'   [$$kcal*cm^2 / molecule$$]'};
        
        
        set(handle.figure,'currentaxes',handle.newtextbox);
        ltxstr=text('interpreter','latex','string',str, 'units','normalized','position',[.05 .5],'fontsize',16);
    end

%--------------------------------------------------------------------------
%Edit boxes for parameters

%Reaction Order
handle.rxnord=uicontrol(...
    'style','edit',...
    'units', 'normalized',...
    'string', '0',...
    'position', [.1 .88 .3 .1],...
    'parent', handle.parameters,...
    'backgroundcolor', 'w');
uicontrol(...
    'style', 'text',...
    'parent', handle.parameters,...
    'units', 'normalized',...
    'string', 'Reaction order, n',...
    'position', [0.1,0.78,0.3,0.1]);

%Pre Exponential
handle.preexp=uicontrol(...
    'style','edit',...
    'units', 'normalized',...
    'string', '1E28',...
    'position', [.6 .88 .3 .1],...
    'parent', handle.parameters,...
    'backgroundcolor', 'w');
uicontrol(...
    'style', 'text',...
    'parent', handle.parameters,...
    'units', 'normalized',...
    'string', 'Pre Exponental, Vn',...
    'position', [0.6,0.78,0.3,0.1]);

% Initial Temperature
handle.inittemp=uicontrol(...
    'style','edit',...
    'units', 'normalized',...
    'string', '100',...
    'position', [.1 .7 .3 .1],...
    'parent', handle.parameters,...
    'backgroundcolor', 'w');
uicontrol(...
    'style', 'text',...
    'parent', handle.parameters,...8
    'units', 'normalized',...
    'string', 'Initial Temp [K]',...
    'position', [0.1,0.67,0.3,0.03]);

% Final Temperature
handle.finaltemp=uicontrol(...
    'style','edit',...
    'units', 'normalized',...
    'string', '1000',...
    'position', [.6 .7 .3 .1],...
    'parent', handle.parameters,...
    'backgroundcolor', 'w');
uicontrol(...
    'style', 'text',...
    'parent', handle.parameters,...
    'units', 'normalized',...
    'string', 'Final Temp [K]',...
    'position', [0.6,0.67,0.3,0.03]);

% beta
handle.beta=uicontrol(...
    'style','edit',...
    'units', 'normalized',...
    'string', '5',...
    'position', [.1 .47 .3 .1],...
    'parent', handle.parameters,...
    'backgroundcolor', 'w');
uicontrol(...
    'style', 'text',...
    'parent', handle.parameters,...8
    'units', 'normalized',...
    'string', 'Beta [K/s]',...
    'position', [0.1,0.37,0.3,0.09]);

% energy cverage dependence
handle.nrgcoverage=uicontrol(...
    'style','edit',...
    'units', 'normalized',...
    'string', '0',...
    'position', [.6 .47 .3 .1],...
    'parent', handle.parameters,...
    'backgroundcolor', 'w');
uicontrol(...
    'style', 'text',...
    'parent', handle.parameters,...
    'units', 'normalized',...
    'string', sprintf('Energy Coverage\nDependence, A'),...
    'position', [0.6,0.37,0.3,0.09]);

% Initial Coverage
handle.initcoverage=uicontrol(...
    'style','edit',...
    'units', 'normalized',...
    'string', '1.5E15',...
    'position', [.35 .3 .3 .1],...
    'parent', handle.parameters,...
    'backgroundcolor', 'w');
uicontrol(...
    'style', 'text',...
    'parent', handle.parameters,...
    'units', 'normalized',...
    'string', 'Initial Coverage [molecules]',...
    'position', [0.35,0.2,0.3,0.1]);
%--------------------------------------------------------------------------
%create coverage checkbox panel
handle.coveragepanel=uipanel(...
    'Title', 'Coverage',...
    'parent',handle.parameters,...
    'backgroundcolor',[.94,.94,.94],...
    'position', [0.05,0.05,0.9,0.15]);

%Create coverage chkboxoxoksskok
handle.percent100 = uicontrol(...
    'parent',handle.coveragepanel,...
    'style','checkbox',...
    'units','normalized',...
    'string','100%',...
    'position',[.15 .1 .2 .8],...
    'value',0);

handle.percent75 = uicontrol(...
    'parent',handle.coveragepanel,...
    'style','checkbox',...
    'units','normalized',...
    'string','75%',...
    'position',[.35 .1 .2 .8],...
    'value',0);

handle.percent50 = uicontrol(...
    'parent',handle.coveragepanel,...
    'style','checkbox',...
    'units','normalized',...
    'string','50%',...
    'position',[.55 .1 .2 .8],...
    'value',0);

handle.percent25 = uicontrol(...
    'parent',handle.coveragepanel,...
    'style','checkbox',...
    'units','normalized',...
    'string','25%',...
    'position',[.75 .1 .2 .8],...
    'value',0);
%--------------------------------------------------------------------------
%create results panel
handle.results=uipanel(...
    'Title', 'Input Ea to Calculate Tp, or Vice Versa',...
    'backgroundcolor',[.94,.94,.94],...
    'position', [0.76,0.2,0.23,0.13]);

%Ea
handle.ea=uicontrol(...
    'style','edit',...
    'units', 'normalized',...
    'string', '30',...
    'position', [.05 .45 .4 .45],...
    'parent', handle.results,...
    'backgroundcolor', 'w');
uicontrol(...
    'style', 'text',...
    'parent', handle.results,...
    'units', 'normalized',...
    'string', 'Activation energy, Ea [kcal]',...
    'position', [.05 .15 .4 .3]);

%Pre Exponential
handle.peakt=uicontrol(...
    'style','edit',...
    'units', 'normalized',...
    'string', '0',...
    'position', [.55 .45 .4 .45],...
    'parent', handle.results,...
    'backgroundcolor', 'w');
uicontrol(...
    'style', 'text',...
    'parent', handle.results,...
    'units', 'normalized',...
    'string', 'Peak Temperature [K] (100% Coverage)',...
    'position', [.55 .03 .4 .43]);

%Print out max desorption for normalizing
handle.maximumyp=uicontrol(...
    'style','edit',...
    'units', 'normalized',...
    'string', '1',...
    'position', [.12 .025 .07 .04],...
    'backgroundcolor', 'w');
uicontrol(...
    'style', 'text',...
    'units', 'normalized',...
    'string', 'Maximum Desorption Rate, Nmax (100% coverage) [molecules/cm^2/s]',...
    'position', [0.055,0.075,0.22,0.02]);

%--------------------------------------------------------------------------
%create plot button
handle.plotit=uicontrol(...
    'style','pushbutton',...
    'units','normalized',...
    'position',[.83 .02 .1 .06],...
    'string','Plot');






%Set Callbacks
set(handle.plotit,'callback',{@plotmyplot})
set(handle.inittemp,'callback',{@axis})
set(handle.finaltemp,'callback',{@axis})
set(handle.nrgcoverage,'callback',{@plotmyplot})
set(handle.beta,'callback',{@plotmyplot})
% set(handle.preexp,'callback',{@plotmyplot})
% set(handle.rxnord,'callback',{@plotmyplot})
set(handle.ea,'callback',{@plotmyplot})
set(handle.initcoverage,'callback',{@plotmyplot})
set(handle.percent100,'callback',{@visibilitycheck})
set(handle.percent75,'callback',{@visibilitycheck})
set(handle.percent50,'callback',{@visibilitycheck})
set(handle.percent25,'callback',{@visibilitycheck})
set(handle.peakt,'callback',{@eafromtp})

%--------------------------------------------------------------------------
%set checkboxes to be checked by default
set(handle.percent100,'value',1);
%--------------------------------------------------------------------------
    function [xx,yyy,Tp,yp]=TPDcalc(Eaa,n,To,Tf,A,B,thetao,v)
        nstep=10000;
        i=0;
        To=100;
        Tf=1000;
        Ea=Eaa*4.18*1000;
        R=8.314;
        oldT=To;
        theta=thetao;
        oldy=0;
        y=0;
        stat=[1*theta,0.75*theta,0.5*theta,0.25*theta];
        h=waitbar(0,'Please wait...')
        for i=1:length(stat)
            waitbar(i/length(stat))
            theta=stat(i);
            thetao=stat(i);
            
            for j=0:nstep;
                T=To+j*(Tf-To)/nstep;
                deltaT=T-oldT;
                Ee=Ea-A*4.184*1000*theta/thetao;
                preexp=v*theta^n/B;
                oldy=y;
                y=preexp*exp(-Ee/(8.314*T));
                yy(j+1,i)=y;
                xx(j+1)=T;
                if y>oldy ;
                    Tp(i)=T;
                    yp(i)=y;
                end;
                theta=theta-y*deltaT;
                oldT=T;
                if theta<=0;
                    theta=0;
                end;
            end
            
        end;
        close(h)
        yp;
        yyy=yy;
        [~,ind]=max(yy);
    end



    function plotmyplot(varargin)
        
        % get the values from all the editboxes:
        [n,v,To,Tf,B,A,thetao,Eaa,Tp]=getstuff(varargin);
        
        %now lets do some plotting....
        cla
        set(handle.figure,'currentaxes',handle.axes)
        if n~=0
            
            [xx,yyy,Tp,yp]=TPDcalc(Eaa,n,To,Tf,A,B,thetao,v);
            handle.plotlines = plot(xx,yyy);
            xlim([To,Tf])
            xlabel('Temperature [K]')
            ylabel('N(t) [molecules/(cm2*s)]')
            title('Temperature Programmed Desorption(TPD)- Desorption Signal')
            legend('show')
            legend('100%','75%','50%','25%')
            legend('location','best')
            
            set(handle.peakt,'string',Tp(1));
            xx=xx';
            data=horzcat(xx,yyy)';
            set(handle.table,'data',data');
            set(handle.maximumyp,'string',yp(1));
            yy=yyy;
            [e1,f1]=max(yy(:,1));
            [~,f2]=max(yy(:,2));
            [e3,f3]=max(yy(:,3));
            [e4,f4]=max(yy(:,4));
            ff=[f1,f2,f3,f4];
            for i = 1:4
                xxzero(i)=xx(ff(i));
            end
            
            set(handle.table2,'data',xxzero)

            
            
        end
        
        
        
        stat=[1,0.75,0.5,25];
        
        if n==0
            h=waitbar(0,'Please wait...');
            [xx,yyy,Tp,yp]=TPDcalc(Eaa,n,To,Tf,A,B,thetao,v);
            yy=yyy;
            [e,f]=size(yy);
            
            for i=1:e-1
                yint(i,1)=trapz(yy(1:i+1,1));
            end
            
            for i=1:4
                for i=1:e-1;
                    if yint(i,1) < 1E15;
                        yint2(i,1)=yint(i);
                        yint3(i,1)=1E15-yint2(i,1);
                    else
                        break
                    end
                end
            end
            stat=[1 0.75 0.5 0.25];
            for j=1:4
                for i=1:e-1;
                    if yint(i,1) < 1E15;
                        yint2(i,j)=yint(i);
                        yint3(i,j)=stat(j)*1E15-yint2(i,j);
                    else
                        yint3(i+1,:)=0;
                        break
                    end
                end
            end
            [f,m]=size(yint3);
            
            for j=1:4;
                for i=1:f;
                    if yint3(i,j) <0;
                        yint3(i,j)=0;
                    end
                end
            end
            
            
            for j=1:4;
                for i=1:f;
                    if yint3(i,j) <0;
                        yint3(i,j)=0;
                    end
                end
            end
            
            
            for j=1:4
                waitbar(j/4)
                for i=1:length(yint3)
                    if yint3(i,j)~=0
                        l=1;
                    else
                        q(1,j)=i;
                        break
                    end
                end
            end
            
            for i=1:4;
                yy(q(i)+1,i)=0;
            end
            
            for j=1:4
                for i=q(j)+1:length(yy);
                    yy(i,j)=0;
                end
            end
            
            for i = 1:4
                xxzero(i)=xx(q(i));
            end
            close(h)
%             stepz=0:10000
%             p=1
%             for i=1:length(xx)
%                 zerostuff(i)=log(yyy(i,1));
%                 oneoverT(i)=1/stepz(i);                      
%             end
%             [slope,intercept]=polyfit(oneoverT,zerostuff,1)
%             p=1
            
            set(handle.figure,'currentaxes',handle.axes)
            handle.plotlines = plot(xx,yy);
            xlim([To,Tf])
            xlabel('Temperature [K]')
            ylabel('N(t) [molecules/(cm2*s)]')
            title('Temperature Programmed Desorption (TPD) - Desorption Signal')
            legend('show')
            legend('100%','75%','50%','25%')
            legend('location','best')
            [f,g]=size(yy);
            p=1;
            dataz=horzcat(xx',yy);
            
            yymax=max(yy(:,1));
            
            set(handle.peakt,'string',xxzero(1))
            set(handle.table2,'data',xxzero)
            set(handle.maximumyp,'string',yymax)
            set(handle.table,'data',dataz)
        end
        
        visibilitycheck;
        plotmyplot2;
        textbox;
        
    end



    function visibilitycheck(varargin)
        try
            stat100 = get(handle.percent100,'value');
            stat75 = get(handle.percent75,'value');
            stat50 = get(handle.percent50,'value');
            stat25 = get(handle.percent25,'value');
            
            if stat100
                set(handle.plotlines(1),'visible','on')
            elseif ~stat100
                set(handle.plotlines(1),'visible','off')
            else
                uiwait(errordlg('this should not happen'))
            end
            
            if stat75
                set(handle.plotlines(2),'visible','on')
            elseif ~stat75
                set(handle.plotlines(2),'visible','off')
            else
                uiwait(errordlg('this should not happen'))
            end
            
            if stat50
                set(handle.plotlines(3),'visible','on')
            elseif ~stat50
                set(handle.plotlines(3),'visible','off')
            else
                uiwait(errordlg('this should not happen'))
            end
            
            if stat25
                set(handle.plotlines(4),'visible','on')
             
            elseif ~stat25
                set(handle.plotlines(4),'visible','off')
            else
                uiwait(errordlg('this should not happen'))
            end
        end
    end

    function axis(varargin)
        set(handle.figure,'currentaxes',handle.axes)
        To = str2double(get(handle.inittemp,'string'));
        Tf = str2double(get(handle.finaltemp,'string'));
        xlim([To,Tf]);
        legend('location','best');
    end
%this function calculates the activation energy from a peak temperature
    function []=eafromtp(varargin)
        
        [n,v,To,Tf,B,A,thetao,Eaa,Tp]=getstuff(varargin);
        if n==1
            Eaaa=lambertw(Tp*v/B)*Tp*8.314/(4.18*1000);
            set(handle.ea,'string',Eaaa)
            
        end
        if n==2
            Eaaa=lambertw(thetao*v*Tp/B)*8.314*Tp/(4.18*1000);
            set(handle.ea,'string',Eaaa)
            
        end
        if n==1/2
            uiwait(errordlg('Can only calculate Ea from Tp for n=[1,2]'))
%             Eaaa=(-1/2*Tp(1)*v/(sqrt(yp(1))*B))*8.314*Tp
        end
        if n==0
            uiwait(errordlg('Can only calculate Ea from Tp for n=[1,2]'))
        end
        
    end

    function plotmyplot2(varargin)
        set(handle.figure,'currentaxes',handle.axes2)
        [n,v,To,Tf,B,A,thetao,Eaa,Tp]=getstuff();
        [xx,yyy,Tp,yp]=TPDcalc(Eaa,n,To,Tf,A,B,thetao,v);
        yy=yyy;
        
        [e,f]=size(yy);
        
        for i=1:e-1;
            yint(i,1)=trapz(yy(1:i+1,1));
        end
        
        stat=[1 0.75 0.5 0.25];
        for j=1:4
            for i=1:e-1;
                if yint(i,1) < thetao;
                    yint2(i,j)=yint(i);
                    yint3(i,j)=stat(j)*thetao-yint2(i,j);
                else
                    yint3(i+1,:)=0;
                    break
                end
            end
        end
        [f,m]=size(yint3);
        p=1;
        for j=1:4;
            for i=1:f;
                if yint3(i,j) <0;
                    yint3(i,j)=0;
                end
            end
        end
        p=1;
        plot(xx(1:f),yint3);
        xlim([To,Tf])
        ylim([0,max(yint3(:,1))+max(yint3(:,1))]);
        xlabel('Temperature [K]');
        ylabel('N(t) [molecules/(cm2*s)]');
        title('Coverage');
        legend('show');
        legend('100%','75%','50%','25%');
        legend('location','best');      
    end



%Gets all the values out of the boxes
    function [n,v,To,Tf,B,A,thetao,Eaa,Tp]=getstuff(varargin)
        n= str2double(get(handle.rxnord,'string'));
        v = str2double(get(handle.preexp,'string'));
        To = str2double(get(handle.inittemp,'string'));
        Tf = str2double(get(handle.finaltemp,'string'));
        B = str2double(get(handle.beta,'string'));
        A= str2double(get(handle.nrgcoverage,'string'));
        thetao = str2double(get(handle.initcoverage,'string'));
        Eaa = str2double(get(handle.ea,'string'));
        Tp = str2double(get(handle.peakt,'string'));
        
    end
        

end