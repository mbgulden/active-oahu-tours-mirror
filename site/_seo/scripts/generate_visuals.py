import os
import matplotlib.pyplot as plt
import numpy as np

# Ensure directory exists
os.makedirs("/home/ubuntu/work/active-oahu-static/site/_seo/images", exist_ok=True)

def generate_comparison_chart():
    # Data from backlinks_overviews.json
    domains = [
        "activeoahutours.com\n(AOT - DA 26)", 
        "kailuabeachadventures.com\n(KBA - DA 32)", 
        "surfnsea.com\n(SNS - DA 36)", 
        "hawaiibeachtime.com\n(HBT - DA 24)", 
        "hawaiiactivities.com\n(HA - DA 48)"
    ]
    ref_domains = [451, 689, 1175, 534, 3526]
    follow_links = [763, 1280, 8959, 1011, 269170]
    
    # We will plot referring domains and follow backlinks (except HawaiiActivities because it scales out the chart)
    domains_subset = domains[:-1]
    ref_domains_subset = ref_domains[:-1]
    
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, ax = plt.subplots(figsize=(9, 5))
    
    colors = ['#ff8c00', '#2ca02c', '#1f77b4', '#d62728']
    bars = ax.bar(domains_subset, ref_domains_subset, color=colors, width=0.5, edgecolor='grey', alpha=0.9)
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, weight='bold')
        
    ax.set_title('Referring Domains Comparison (Direct Competitors)', fontsize=14, pad=15, weight='bold', color='#333333')
    ax.set_ylabel('Number of Referring Domains', fontsize=11, labelpad=10)
    ax.set_ylim(0, 1400)
    
    plt.tight_layout()
    plt.savefig("/home/ubuntu/work/active-oahu-static/site/_seo/images/backlink-comparison.png", dpi=150)
    plt.close()
    print("Saved backlink-comparison.png")

def generate_workflow_chart():
    # Let's create an outreach workflow diagram
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    
    # Draw boxes and text representing steps
    steps = [
        "1. Identify Gaps\n(Competitor backlink analysis\n& target matching)",
        "2. Asset Creation\n(Create maps, tide charts,\nand safety guides)",
        "3. Tiered Prospecting\n(Segment lists: Tier 1, 2, 3\nby DA & Relevance)",
        "4. Personalized Pitching\n(Send tailored outreach emails\nusing tested templates)",
        "5. Multi-touch Follow-up\n(3 contact attempts over\n10 days to maximize CTR)",
        "6. Link Placement & Monitor\n(Track live backlinks & DA\ngrowth to target DA 35+)"
    ]
    
    # Draw boxes
    for i, step in enumerate(steps):
        row = i // 3
        col = i % 3
        
        # Position
        x = col * 3.5 + 0.5
        y = 3.5 - row * 2.5
        
        # Drawing bounding box
        rect = plt.Rectangle((x, y), 2.8, 1.8, facecolor='#f4f7f6', edgecolor='#1f77b4', linewidth=2)
        ax.add_patch(rect)
        
        # Text inside
        ax.text(x + 1.4, y + 0.9, step, ha='center', va='center', fontsize=9, weight='bold', color='#2c3e50')
        
        # Draw arrows between boxes
        if col < 2:
            ax.annotate('', xy=(x + 2.8, y + 0.9), xytext=(x + 3.5, y + 0.9),
                        arrowprops=dict(arrowstyle="<-", color='#ff8c00', lw=2))
        elif row == 0 and col == 2:
            # Draw arrow down to next row
            ax.annotate('', xy=(x + 1.4, y), xytext=(x + 1.4, y - 0.7),
                        arrowprops=dict(arrowstyle="<-", color='#ff8c00', lw=2))
            
    # Arrow from box 5 to box 4 (reverse order on row 1)
    # Wait, row 1 order: step 3, 4, 5. Step 3 is index 3, Step 4 is index 4, Step 5 is index 5
    # Let's draw arrows for row 1 from index 5 to 4 and 4 to 3 (which is leftwards)
    # Positions:
    # index 3: col 0, row 1. x = 0.5, y = 1.0
    # index 4: col 1, row 1. x = 4.0, y = 1.0
    # index 5: col 2, row 1. x = 7.5, y = 1.0
    
    # Arrow from 4 to 5 (or from index 3 to 4, 4 to 5):
    # Wait, let's keep the flow col 0 -> col 1 -> col 2 on row 1 too:
    # index 3 -> index 4: arrow from col 0 to col 1
    # index 4 -> index 5: arrow from col 1 to col 2
    # But wait, index 2 was col 2, row 0 (x=7.5, y=3.5).
    # index 3 is col 0, row 1 (x=0.5, y=1.0).
    # Arrow from index 2 to index 3 needs to go from right side down-left to left side.
    # Let's draw a curved arrow from index 2 to index 3
    ax.annotate('', xy=(0.5 + 1.4, 1.0 + 1.8), xytext=(7.5 + 1.4, 3.5),
                arrowprops=dict(arrowstyle="->", color='#ff8c00', lw=2, connectionstyle="arc3,rad=-0.2"))
    
    # Arrow from 3 to 4 (col 0 to col 1)
    ax.annotate('', xy=(4.0, 1.0 + 0.9), xytext=(3.3, 1.0 + 0.9),
                arrowprops=dict(arrowstyle="->", color='#ff8c00', lw=2))
    
    # Arrow from 4 to 5 (col 1 to col 2)
    ax.annotate('', xy=(7.5, 1.0 + 0.9), xytext=(6.8, 1.0 + 0.9),
                arrowprops=dict(arrowstyle="->", color='#ff8c00', lw=2))

    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)
    ax.set_title("Digital PR & Link Acquisition Workflow", fontsize=14, weight='bold', pad=20, color='#333333')
    
    plt.tight_layout()
    plt.savefig("/home/ubuntu/work/active-oahu-static/site/_seo/images/outreach-workflow.png", dpi=150)
    plt.close()
    print("Saved outreach-workflow.png")

if __name__ == "__main__":
    generate_comparison_chart()
    generate_workflow_chart()
